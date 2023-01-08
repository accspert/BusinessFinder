import os
from datetime import datetime
from datetime import timedelta  

from cryptography.fernet import Fernet

def make_a_expire_date():
    if not os.path.isfile('.\\key.key'):
        
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
            key_file.close()
        date_start = str(datetime.date(datetime.now() + timedelta(days=10)))
        fernet = Fernet(key)
        date_encr = fernet.encrypt(date_start.encode())
        
        with open("hanso.txt", "wb") as date_file:
            date_file.write(date_encr)
            date_file.close()
def get_expire_date():
    key_file = open('key.key', 'rb')
    key = key_file.read()
    key_file.close
    
    date_file = open('hanso.txt' ,'rb')
    date_dec = date_file.read()
    date_file.close()
    
    fernet = Fernet(key)
    date_start = fernet.decrypt(date_dec).decode()
    return datetime.strptime(date_start, '%Y-%m-%d').date()
    
