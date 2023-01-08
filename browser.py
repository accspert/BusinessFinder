import os
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    
    Chrome_UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'

    def __init__(self):
        self.driver=None
        self.proxyExtensionPath=''
        self.packedExtension=list()
     
    def startBrowser(self,path,url='',userAgent='',setMaximizeWindow=True,headless=False):
        if self.proxyExtensionPath:
            self.packedExtension.append(self.proxyExtensionPath)
        options=self.__getArguments(userAgent,headless)
        self.driver=webdriver.Chrome(path,options=options)
        if setMaximizeWindow==True:
            self.maximizeWindow()
        if isinstance(url,str) and url:
            self.getPage(url)
        
    def getPage(self,url):
        self.driver.get(url)
        
    def maximizeWindow(self):
        self.driver.maximize_window()
    
    def getOpenedTabsCount(self)->int():
        return len(self.driver.window_handles)
    
    def closeTabeByIndex(self,index):
        self.switchTab(index)
        self.driver.close()
        if self.proxyExtensionPath:
            os.remove(self.proxyExtensionPath)

    def switchTab(self,tabNum):   
        self.driver.switch_to.window(self.driver.window_handles[tabNum]) 
    
    def addPackedExtension(self,packedExtensions):
        """
        Add packed extension to the browser.Extension must be packed i.e .crx files and in the same folder

        Args:
            nameExtensions (list): List containing name of the packed extension
        """
        self.packedExtension=packedExtensions
            
    def sendKeysByName(self,name,key) -> bool():
        try:
            self.driver.find_element_by_name(name).send_keys(key)
            return True
        except:
            pass
        return False
             
    def sendKeysByXpath(self,xpath,key) -> bool():
        try:
            self.driver.find_element_by_xpath(xpath).send_keys(key)
            return True
        except:
            pass
        return False
    
    def sendKeysByID(self,id,key) -> bool():
        try:
            self.driver.find_element_by_id(id).send_keys(key)
            return True
        except:
            pass
        return False
    
    def isClickableElementFoundByXpath(self,xpath,time):
        return WebDriverWait(self.driver,time).until(EC.element_to_be_clickable((By.XPATH,xpath)))

    def clickButtonByName(self,name,time=10) -> bool():
        try:
            element=WebDriverWait(self.driver,time).until(EC.element_to_be_clickable((By.NAME,name)))
            element.click()
            return True
        except:
            pass
        return False
    
    def clickButtonByXpath(self,xpath,time=10) -> bool():
        try:
            element=self.isClickableElementFoundByXpath(xpath,time)
            element.click()
            return True
        except:
            pass
        return False
            
    def clickButtonByID(self,id,time=10) -> bool():
        try:
            element=WebDriverWait(self.driver,time).until(EC.element_to_be_clickable((By.ID, id)))
            element.click()
            return True
        except Exception as exc:
            pass
        return False
                 
    def clickButtonByClassName(self,className,time=10) -> bool():
        try:
            element=WebDriverWait(self.driver,time).until(EC.element_to_be_clickable((By.CLASS_NAME,className)))
            element.click()
            return True
        except:
            pass
        return False

    def getElementByClassName(self,className,time=10):
        try:
            element=WebDriverWait(self.driver,time).until(EC.presence_of_element_located((By.CLASS_NAME,className)))
            return element
        except:
            pass

    def getElementByID(self,id,time=10):
        try:
            element=WebDriverWait(self.driver,time).until(EC.presence_of_element_located((By.ID,id)))
            return element
        except:
            pass
    

    def executeScript(self,script):
        self.driver.execute_script(script)
    
    def __getArguments(self,userAgent='',headless=False):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument("--output=/dev/null")
        # Argument for english language
        options.add_argument("--lang=en-ca")
        ###########################################################################
        options.add_argument("--disable-user-media-security=true")
        ###########################################################################
        
        
        # Remove automation header
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        if isinstance(userAgent,str) and isinstance:
            options.add_argument(f"user-agent={userAgent}")
        if headless==True:
            options.add_argument('--headless')
        if len(self.packedExtension)>0:
            for packedExtension in self.packedExtension:
                options.add_extension(packedExtension)
        return options
    
    def addAuthenticateProxy(self,proxyHost,proxyPort,proxyUser,proxyPassword):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]
                }
              };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxyHost,proxyPort,proxyUser,proxyPassword)
        pluginfile = self.__getProxyExtensionName()
        self.proxyExtensionPath=pluginfile
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
    
    def __getProxyExtensionName(self):
        i=0
        proxyExtensionPath=f'proxyExtension{i}.zip'
        while os.path.exists(proxyExtensionPath):
            i+=1
            proxyExtensionPath=f'proxyExtension{i}.zip'
        return proxyExtensionPath