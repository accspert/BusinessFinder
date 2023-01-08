import json
from time import sleep
from random import randint
from browser import Browser
from selenium.webdriver.common.keys import Keys

url='https://www.bing.com/maps'
# Function to search the keyword in the map
def isSearchKeyword(browser:Browser,keyword)->bool:
    try:
        searchBox=browser.getElementByID('maps_sb')
        if searchBox:
            searchBox.clear()
            searchBox.send_keys(keyword)
            searchBox.send_keys(Keys.RETURN)
            browser.driver.implicitly_wait(5)
            sleep(randint(5,9))
            return True
    except:
        pass
    return False     
# Check whethert next page available or not
def isNextPage(browser)->bool:
    if browser.clickButtonByClassName('bm_rightChevron'):
        sleep(randint(5,9))
        return True
    return False
# Scrape data from card
def getDataFromContainer(cardContainer)->list:
    def getData(index)->str:
        try:
            return data[index]
        except:
            pass
        return '' 
    try:
        data=json.loads(cardContainer.get_attribute('data-entity'))
        data=data['entity']
        name=getData('title')
        address=getData('address')
        phone=getData('phone')
        website=getData('website')
        return [name,address,phone,website,'']
    except:
        pass
    return []
# Function to get data from google maps
def getDataFromBingMaps(places, query,maxCount):
    # Main Start from here    
    keyword = query+' '+places
    # Start the browser
    browser=Browser()
    browser.startBrowser('chromedriver.exe',url,Browser.Chrome_UserAgent,False,True)
    browser.clickButtonByXpath('/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button')# for google term os services unomment
    
    browser.driver.implicitly_wait(5)
    data=list()
    browser.clickButtonByID('bnp_btn_accept') # for bing terms of services
    # Check keyword searched succesfuly or not
    if isSearchKeyword(browser,keyword):
        
        count=0
        while count<maxCount:
            cardContainers=browser.driver.find_elements_by_class_name('listings-item')
            if cardContainers==None or len(cardContainers)==0:
                break
            while count<len(cardContainers) and count<=maxCount:
                dt=getDataFromContainer(cardContainers[count])
                if(len(dt)>0):
                    data.append(dt)
                count+=1
            if(count<maxCount):
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

