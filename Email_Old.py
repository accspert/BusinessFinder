import math
import urllib.request
import time
import re

import requests
from fake_useragent import UserAgent
from socket import timeout
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pandas as pd

COUNT = 0
URLS = ["https://www.parkersupportservices.co.uk/" ]
imageExt = ["jpeg", "exif", "tiff", "gif", "bmp", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat",
            "bpg", "cgm", "svg"]
ua = UserAgent()
EMAILS = []
REJECTED_URLS = []
DEAD_URLS = []
IDX = 0
TO_FIND = ['contact', 'contact-us', 'contact_us', 'contactus', 'contact.html']
MAIN_URL = ""

def method1(url, two=True):
    global COUNT
    url = url.replace(" ", "")
    if "http" not in url:
        if "www." not in url:
            url = "www." + url
        url = "http://" + url
    if "www." in url:
        temp_url = url[url.find(".") + 1:]
    else:
        temp_url = url[url.find("//") + 2:]
    temp_url = temp_url[:temp_url.find(".")]
    print(url)
    try:
        count = 0
        listUrl = []
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': ua.random
            })

        try:
            conn = urllib.request.urlopen(req, timeout=10)

        except timeout:
            raise ValueError('Timeout ERROR')

        except (HTTPError, URLError):
            raise ValueError('Bad Url...')

        status = conn.getcode()
        contentType = conn.info().get_content_type()

        if (status != 200 or contentType == "audio/mpeg"):
            raise ValueError('Bad Url...')

        try:
            html = conn.read().decode('utf-8')
        except:
            headers = {'Accept-Encoding': 'identity'}
            r = requests.get(url, headers=headers)
            html = r.text

        emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)
        new_emails = []
        for email in emails:
            if (email not in listUrl and email[-3:] not in imageExt):
                count += 1
                listUrl.append(email)
                new_emails.append(email)
        if count == 0:
            if html.find("email-protection#") != -1:
                count += 1
                e = html[html.find("email-protection#") + 17:]
                e = e[:e.find('"')]
                de = ""
                k = int(e[:2], 16)
                for i in range(2, len(e) - 1, 2):
                    de += chr(int(e[i:i + 2], 16) ^ k)
                EMAILS.append(de)
            else:
                if two: REJECTED_URLS.append(url)
        else:
            COUNT += 1
            count = 0
            for mail in new_emails:
                if temp_url.lower() in mail:
                    count += 1
                    EMAILS.append(mail)
                    break
    except KeyboardInterrupt:
        REJECTED_URLS.append(url)
        pass

    except Exception as e:
        DEAD_URLS.append(url)
        pass


def method2(url):
    url = url.replace(" ", "")
    if "http" not in url:
        if "www." not in url:
            url = "www." + url
        url = "http://" + url
    original_url = url
    if "www." in url:
        temp_url = url[url.find(".") + 1:]
    else:
        temp_url = url[url.find("//") + 2:]
    temp_url = temp_url[:temp_url.find(".")]
    # print(temp_url)
    try:
        count = 0
        listUrl = []
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': ua.random
            })

        try:
            conn = urllib.request.urlopen(req, timeout=10)

        except timeout:
            raise ValueError('Timeout ERROR')

        except (HTTPError, URLError):
            raise ValueError('Bad Url...')

        status = conn.getcode()
        contentType = conn.info().get_content_type()

        if (status != 200 or contentType == "audio/mpeg"):
            raise ValueError('Bad Url...')

        try:
            html = conn.read().decode('utf-8')
        except:
            headers = {'Accept-Encoding': 'identity'}
            r = requests.get(url, headers=headers)
            html = r.text

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)

        for email in emails:
            if (email not in listUrl and email[-3:] not in imageExt):
                count += 1
                listUrl.append(email)

        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('a')
        mailtos = soup.select('a[href^=mailto]')
        if mailtos:
            for i in mailtos:
                href = i['href']
                try:
                    str1, str2 = href.split(':')
                except ValueError:
                    break
                EMAILS.append(str2)
        else:
            # print("They will be analyzed " + str(len(links) + 1) + " Urls...")
            time.sleep(2)
            for tag in links:
                link = tag.get('href', None)
                if link is not None:
                    try:
                        if link[0] == '/':
                            link = original_url + link
                        if link.find(temp_url) != -1 and link.find("contact") != -1:
                            method1(link, False)

                    except Exception:
                        pass

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)
        pass


def get_email(url, secondTime=False):
    global EMAILS
    method1(url)
    if len(EMAILS) == 0 and not secondTime:
        method2(url)
    return_emails = EMAILS
    EMAILS = []
    if len(return_emails) > 0:
        return list(return_emails)[0]


def email_extract(url, searchDepth = False):
    global TO_FIND
    if url.find("//") != -1:
        url = url[url.find("//")+2:]
        if url.find('/') != -1:
            url = url[:url.find('/')]
    elif url.find('/') != -1:
        url = url[:url.find('/')]
    print(url)
    e_mail = get_email(url, searchDepth)
    if e_mail:
        return e_mail
    if url[-1] != '/':
        url += '/'
    for i in range(0, 5):
        e_mail = get_email(url + TO_FIND[i], True)
        if e_mail:
            return e_mail
    return e_mail

