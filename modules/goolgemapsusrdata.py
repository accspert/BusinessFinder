from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
   
usrdatafolder='C:\\usrrdata'
options.add_argument(f"user-data-dir={usrdatafolder}")
driver = webdriver.Chrome(options=options)



driver.get("https://www.google.com/maps")    