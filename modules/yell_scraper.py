import bs4
import requests

API_KEY = 'a7d43ec4c99806f28a1492c514938339'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
                         'Version/9.0.2 Safari/601.3.9'}
DATA = []
SCRAPE_WITH_API = False


def get_response(new_url):
    print(new_url)
    if SCRAPE_WITH_API:
        payload = {'api_key': API_KEY, 'url': new_url}
        new_response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
    else:
        new_response = requests.get(new_url, headers=headers)
    return new_response


def scrape_yell(location, looking_for):
    DATA = []
    looking_for = looking_for.replace(' ', '%20')
    location = location.replace(', ', '%2C%20')
    location = location.replace(' ', '%20')
    url = f'https://www.yell.com/ucs/UcsSearchAction.do?keywords={looking_for}&location={location}&scrambleSeed=509559697&pageNum='
    for page in range(1, 5):
        url1 = url + str(page)
        req = get_response(url1)
        print(req)
        if not req.ok:
            return DATA
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        product = soup.findAll('div', 'row businessCapsule--mainRow')
        for x in product:
            try:
                name = x.find('h2', 'businessCapsule--name text-h2').text
            except:
                name = 'None'
            try:
                address = x.find('span', {'itemprop': 'address'}).text
            except:
                address = 'None'
            try:
                telp = x.find('span', 'business--telephoneNumber').text
            except:
                telp = 'None'
            try:
                web = x.find('a', {'rel': 'nofollow noopener'})['href'].split('?')[0].replace('https://', '').replace(
                    'http://', '').replace('http:', '').replace('www.', '')
            except:
                web = "None"
            address = address.replace("\n", "")
            address = address.replace('"',  "")
            
            DATA.append([name, address, telp, web,''])
    return DATA
