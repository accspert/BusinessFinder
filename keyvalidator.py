import requests
from ErrorLogger import *
import traceback


def verify_account_key(account_key_to_check):
    try:
        website = "accspert.com" #for example, niftynicktools.com
        consumer_key = "ck_c50bf55ba54b1d2c1c07d719093c0da7d09c814c" #the consumer_key given to you when you establish your API with License Manager
        consumer_secret = "cs_da60f389b8a9dfa273bfd2479fafa54807292a12" #the consumer_secret given to you when you establish your API with License Manager
        url = "https://" + website + "/wp-json/lmfwc/v2/licenses/activate/" + account_key_to_check + "?consumer_key=" + \
              consumer_key + "&consumer_secret=" + consumer_secret
        # url = "https://" + yourwebsite + "/wp-json/lmfwc/v2/licenses/validate/" + account_key_to_check + "?consumer_key=" + \
        #       consumer_key + "&consumer_secret=" + consumer_secret
    
        verification_json = requests.get(url, headers={"User-Agent": "Egon"}).json()
        try:
            if verification_json['success'] == True:
                return True
        except:
            return False
        
    except Exception as e:
        ErrorLogger.WriteError(traceback.format_exc())
        QtWidgets.QMessageBox.critical(None, 'Exception raised', format(e))

