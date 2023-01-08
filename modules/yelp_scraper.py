from bs4 import BeautifulSoup
from lxml import etree
import requests

API_KEY = 'a7d43ec4c99806f28a1492c514938339'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
                         'Version/9.0.2 Safari/601.3.9'}
DATA = []
business_website = []
Phone_number = []
Address = []
Name = []
web = False
phone = False
address = False
SCRAPE_WITH_API = False


def check(res, found):
    global web, phone, address
    if res.find("Business website") != -1:
        business_website.append(found[0][0][1][0].text)
        web = True
    if res.find("Phone number") != -1:
        Phone_number.append(found[0][0][1].text)
        phone = True
    if res.find("Get Directions") != -1:
        Address.append(found[0][0][1].text)
        address = True


def get_response(new_url):
    if SCRAPE_WITH_API:
        payload = {'api_key': API_KEY, 'url': new_url}
        new_response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
    else:
        new_response = requests.get(new_url, headers=headers)
    return new_response


def get_data(web_name):
    global web, phone, address
    try:
        new_url = 'https://www.yelp.com' + web_name
        new_response = get_response(new_url)
        if new_url.find('/biz/') == -1 :
            new_url = str(new_response.content)
            x = new_url.find('location.replace("') + 18
            new_url = new_url[x:]
            new_url = new_url[:new_url.find('");')]
            new_response = get_response(new_url)
        print(new_url)
        if not new_response.ok:
            return False
        new_soup = BeautifulSoup(new_response.content, 'lxml')
        dom = etree.HTML(str(new_soup))
        one = dom.xpath(
            '/html/body/div[2]/div[2]/yelp-react-root/div[1]/div[4]/div/div/div[2]/div/div[2]/div/div/section[1]')
        two = dom.xpath(
            '/html/body/div[2]/div[2]/yelp-react-root/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div/section[1]')
        if len(one) < len(two):
            one = two
        if one:
            web = phone = address = False
            for i in range(len(one[0][0])):
                check(str(etree.tostring(one[0][0][i], pretty_print=True, method="html")), one[0][0][i])
            if not web:
                business_website.append("-")
            if not address:
                Address.append("-")
            if not phone:
                Phone_number.append("-")
    except:
        pass
    return True


def init(url):
    response = get_response(url)
    print(response)
    if not response.ok:
        return False
    response_ok = True
    soup = BeautifulSoup(response.content, 'lxml')
    for item in soup.select('[class*=container]'):
        if item.find('h4'):
            for a in item.find('h4').find_all('a', href=True):
                    Name.append(a['name'])
                    response_ok = get_data(a['href'])
                    break
        if not response_ok:
            return False
    return True


def scrape_yelp(location, looking_for):
    DATA=[]
    looking_for = looking_for.replace(' ', '%20')
    location = location.replace(', ', '%2C%20')
    location = location.replace(' ', '%20')
    print(f"You are looking for -> {looking_for}")
    print(f"At Location -> {location}")
    url1 = f'https://www.yelp.com/search?find_desc={looking_for}&find_loc={location}'
    for i in range(0, 5):
        value = init(url1 + f"&start={i * 10}")
        if not value:
            break
    for i in range(len(business_website)):
        DATA.append([Name[i], Address[i], Phone_number[i], business_website[i],''])
    return DATA
