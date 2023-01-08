import os
import pandas as pd
from time import sleep
from random import randint
from browser import Browser
url='https://www.google.com/maps'
# Get search keyword from the user and check all program files
def getInput()->tuple:
    # Check chrome browser exists or not
    if not os.path.exists('chromedriver.exe'):
        input("chromedriver.exe Not Found\nPress Any Key TO Exit->")
        exit(1)
    keyword=input('Input Search Keywords[e.g:real estate, new york] -> ')
    maxCount=int(input('Input Max Count To Get Items [e.g:1000] -> '))
    if not keyword:
        input("Invalid Input\nPress Any Key To Exit->")
        exit(1)
    return keyword,maxCount
# Function to search the keyword in the map
def isSearchKeyword(browser,keyword)->bool:
    if  browser.sendKeysByID('searchboxinput',keyword) and browser.clickButtonByID('searchbox-searchbutton',5):
        browser.driver.implicitly_wait(5)
        sleep(randint(5,9))
        return True
    return False
# Check whethert next page available or not
def isNextPage(browser)->bool:
    if browser.clickButtonByXpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/div/button[2]'):
        sleep(randint(5,9))
        return True
    return False
# Scrape data from the bottom pane
def scrapeDataFromBottomPane(browser,data,maxCount):
    bottomPane=browser.getElementByClassName('jiAh7-bottom-pane')
    sleep(randint(5,9))
    # Get all searched elements containers
    containerElements=bottomPane.find_elements_by_class_name('jpDWw-HiaYvf')
    for containerElement in containerElements:
        if len(data)>maxCount:
            break
        try:
            browser.driver.execute_script("arguments[0].click();",containerElement)
        except:
            continue
        browser.driver.implicitly_wait(5)
        sleep(randint(5,9))
        try:
            try:
                header=browser.driver.find_element_by_class_name('x3AX1-LfntMc-header-title-ij8cu').text
            except:
                continue
            header=header.split('\n')
            try:
                name=header[0]
                buisnessName=header[3]
            except:
                pass
            address=''
            website=''
            phone=''
            email=''
            sleep(3)
            containerElements=browser.driver.find_elements_by_class_name('dqIYcf-RWgCYc-text')
            for containerElement in containerElements:
                try:
                    label=containerElement.find_element_by_tag_name('button').get_attribute('aria-label')
                    if label:
                        if 'Address' in label:
                            address=label.split(':')[1]
                        elif 'Website' in label:
                            website=label.split(':')[1]
                        elif 'Email' in label:
                            email=label.split(':')[1]
                        elif 'Phone' in label:
                            phone=label.split(':')[1]
                except:
                    pass
            data.append([name,address,phone,website,email,])
        except:
            pass
# Function to get data from google maps
def getDataFromGoogleMaps(places, query,maxCount):
    data=[]
    # Main Start from here    
    keyword = query + ',' + places
    # Start the browser
    browser=Browser()
    browser.startBrowser('chromedriver.exe',url,Browser.Chrome_UserAgent,False)
    browser.clickButtonByXpath('/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button')
    browser.driver.implicitly_wait(5)
    data=list()
    # Check keyword searched succesfuly or not
    if isSearchKeyword(browser,keyword):
        # Uncomment below line if direct save to file for header writing
        # data.append(['Name','BuisnessName','Website','Address','Phone','Email'])
        while True:
            # Click any item on the scroll page
            if not browser.clickButtonByClassName('section-scrollbox',20):
                # Click not successfull break
                print("[ERROR] : Scroll Page Not Found")
                break
            browser.driver.implicitly_wait(5)
            sleep(randint(5,9))
            try:
                scrapeDataFromBottomPane(browser,data,maxCount)
            except Exception as exc:
                print(exc)
                pass
            if len(data)>maxCount:
                break
            # Back to resuts page
            if not browser.clickButtonByXpath('/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[1]/button'):
                # Click not successfull break
                print("[ERROR] : Back to results button Not Found")
                break
            browser.driver.implicitly_wait(5)
            sleep(randint(5,9)) 
            # GO to next page if next page not found break
            if not isNextPage(browser):
                break
            else:
                browser.driver.implicitly_wait(5)
                sleep(randint(5,9))
    try:
        browser.driver.close()
    except:
        pass
    return data