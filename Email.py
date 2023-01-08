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

e_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
imageExt = ["jpeg", "exif", "tiff", "gif", "bmp", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat",
            "bpg", "cgm", "svg", "io"]
ua = UserAgent()
EMAILS = []
REJECTED_URLS = []
DEAD_URLS = []
IDX = 0
TO_FIND = ['contact', 'contact-us', 'contact_us', 'contactus', 'contact.html']
MAIN_URL = ""

def home_page(home_url):
    emails = []
    headers = {'User-agent': str(ua.random)}
    try:
        first_main_page = requests.get(home_url, headers=headers, timeout=10)
        main_page = requests.get(first_main_page.url, headers=headers, timeout=10)
        soup = BeautifulSoup(main_page.content, "lxml")
        a_elements = soup.find_all("a")
        for single_a in a_elements:
            if "data-cfemail" in str(single_a):
                print("data-cfemail")
                a_splitted = str(single_a).split(' ')
                for encoded_a in a_splitted:
                    if "data-cfemail" in encoded_a:
                        counter = 0
                        encoded_find = False
                        while encoded_find == False:
                            try:
                                if encoded_a[counter].endswith("="):
                                    encoded = encoded_a[counter + 1]
                                    encoded_find = True
                                else:
                                    counter += 1
                            except:
                                break

                        try:
                            r = int(encoded[:2],16)
                            decode_email = ''.join([chr(int(encoded[i:i+2], 16) ^ r) for i in range(2, len(encoded), 2)])
                            if decode_email not in email_list:
                                email_list.append(decode_email)
                                break
                        except (ValueError):
                            pass
            elif "mailto" in str(single_a):
                a_splitted = str(single_a).split(' ')
                for single_a_s in a_splitted:
                    if "mailto" in single_a_s:
                        front_remove = single_a_s[(single_a_s.find('"') + 9):]
                        clean_email = front_remove[:(front_remove.find('"'))]
                        emails.append(clean_email)
                        break
        
        for email in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', main_page.text):
            if email not in emails:
                splitted_email = email.split(".")
                if splitted_email[len(splitted_email)-1] not in imageExt:
                    emails.append(email)
    except:
        pass
    
    return emails

def contact_pages(main_url):
    print("Clean:", str(main_url))
    global email_list
    links = []
    tries = 1
    while tries <= 2 or len(links) >= 1:
        try:
            print("Trying")
            headers = {'User-agent': str(ua.random)}
            first_main_page = requests.get(main_url, headers=headers, timeout=10)
            main_page = requests.get(first_main_page.url, headers=headers, timeout=10)
            soup = BeautifulSoup(main_page.content, 'lxml')
            for link in soup.findAll('a'):
                if "contact" in str(link):
                    if link not in links:
                        links.append(link.get('href'))
            if len(links) >= 1 or main_page.status_code == "200":
                break
            tries += 1
        except:
            break
    return links


def email_extract(current_url):
    valid_email = True
    if current_url == "-" or current_url.endswith("...") == True or current_url.endswith("…") or current_url == "None":
        valid_email = False
        
    if valid_email == False:
        return "-"
    else:
        email_list = []
        clean_url = None
        print(current_url)
        if current_url.startswith("http"):
            if not current_url.endswith("/"):
                clean_url = str(current_url) + "/"
            else:
                clean_url = str(current_url)
        else:
            if not current_url.endswith("/"):
                clean_url = "http://" + str(current_url) + "/"
            else:
                clean_url = "http://" + str(current_url)

                    
        print(clean_url)
        
        headers = {'User-agent': str(ua.random)}
        r_clean_url = None
        for i in range(5):
            try:
                first_clean_url = requests.get(clean_url, headers=headers, timeout=10)
                r_clean_url = requests.get(first_clean_url.url, headers=headers, timeout=10)
            except:
                pass
        if r_clean_url == None:
            return "-"
        
        print("Contact start")
        contact_urls = contact_pages(r_clean_url.url)
        print("Contact end")
        
        print(contact_urls)
        clean_url = r_clean_url.url
        if len(list(contact_urls)) >= 1:
            for contact in contact_urls:
                print("Contact")
                tries = 1
                while len(email_list) == 0 and tries <= 2:
                    print("trying")
                    if len(email_list) == 0:
                        new_url = None
                        if contact.startswith("http"):
                            new_url = contact
                        else:
                            if clean_url.startswith("http"):
                                new_url = str(clean_url) + str(contact)
                            else:
                                new_url = "http://" + str(clean_url) + str(contact)
                        
                        dot_split = new_url.split(".")
                        new_list = [dot_split[0]]
                        for parts in range(1, len(dot_split)):
                            new_part = dot_split[parts].replace("//", "/")
                            new_list.append(new_part)
                        new_url = ".".join(new_list)

                        headers = {'User-agent': str(ua.random)}
                        
                        first_page = requests.get(new_url, headers=headers, timeout=10)
                        page = requests.get(first_page.url, headers=headers, timeout=10)
                        print(page.url)
                        print(str(page.status_code))
                        if str(page.status_code) == "200":
                            for email in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', page.text):
                                if email not in email_list:
                                    splitted_email = email.split(".")
                                    if splitted_email[len(splitted_email)-1] not in imageExt:
                                        email_list.append(email)
                                        break

                            html = page.content
                            soup = BeautifulSoup(html, 'lxml')
                            a_elements = soup.find_all('a')
                            a_list = str(a_elements).split()
                            for single_a in a_list:
                                if len(single_a) > 3:
                                    splitted_a = single_a.split(" ")
                                    for items_a in splitted_a:
                                        if "mailto" in items_a:
                                            front_remove = items_a[(items_a.find('"') + 9):]
                                            clean_email = front_remove[:(front_remove.find('"'))]
                                            email_list.append(clean_email)
                                            break
                                        
                                        elif "data-cfemail" in str(items_a):
                                            href = str(items_a).split('"')
                                            encoded_find, encoded = False, None

                                            counter = 0
                                            while encoded_find == False:
                                                try:
                                                    if href[counter].endswith("="):
                                                        encoded = href[counter + 1]
                                                        encoded_find = True
                                                    else:
                                                        counter += 1
                                                except:
                                                    break

                                            try:
                                                r = int(encoded[:2],16)
                                                decode_email = ''.join([chr(int(encoded[i:i+2], 16) ^ r) for i in range(2, len(encoded), 2)])
                                                if decode_email not in email_list:
                                                    email_list.append(decode_email)
                                                    break
                                            except (ValueError):
                                                pass
                    else:
                        break
                    tries += 1
        else:
            home_emails = home_page(clean_url)
            print(home_emails)
            for single_email in home_emails:
                for email in re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', single_email):
                    email_list.append(email)
                    break

        if len(email_list) >= 1:
            return email_list[0]
        else:
            return "-"

#print(gEmail("sos-officesupplies.co.uk"))