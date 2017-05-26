from .imports import * 
import sys, os, shutil
import configparser
from cryptography.fernet import Fernet
import time 

root_url = 'https://www.kaggle.com'
login_url = '/account/login'
test_url = '/c/titanic'
rules = '/rules'
data = '/data'

config_path = click.get_app_dir('kli') + '/kli.ini'

class config(object):
    def __init__(self, *args, **kwargs): 

        # if the file location doesnt exit
        if not os.path.isfile(config_path):
            os.makedirs(click.get_app_dir('kli'), exist_ok=True)
            self.make_config()
            self.config_filepath = config_path
            self.config_file = self.config_load()

        # if the file location exists, check if its empty
        else:
            # check if its empty, make one if it is
            if os.stat(config_path).st_size == 0: 
                self.make_config()
                self.config_filepath = config_path
                self.config_file = self.config_load()
            else:
                # if its not empty, rename config path, and load config file
                self.config_filepath = config_path
                self.config_file = self.config_load()
        super(config, self).__init__()
    
    def make_config(self):
        conf = configparser.ConfigParser()
        conf.optionxform = str

        conf.add_section('UserSettings')
        key = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
        conf['UserSettings']['key'] = key

        # below password is already hashed, default unhashed password = password 
        conf['UserSettings']['Password'] = 'gAAAAABZC018YC8y4q9gdnI-xIuNXeySuP-hOIqkqTkKxAiSQOZvGPToU8wan6_xgm8bXk-KdrBdJjsdhGOnDv1PC5ipU5FbqQ==' 
        conf['UserSettings']['UserName'] = 'UserName'
        conf['UserSettings']['action'] = 'login'

        with open(config_path, 'w') as f: 
            conf.write(f)

        print("""
        The config file was restored to its default value (or a new config file was made). 
        You can reset your user settings via the command 'kl setup'.
        """)

    def config_load(self):
        if not os.path.isfile(self.config_filepath):
            print("\nConfig file not found in %s \n" %config_path)
            print("""You can make an empty config file in the above location, or
run the command 'kli mconfig', which will make one for you.\n""")
            sys.exit(0)

        conf= configparser.ConfigParser()
        conf.optionxform = str
        conf.read(self.config_filepath)

        try:
            cipher_suite = Fernet(str.encode(conf['UserSettings']['key']))
        except (KeyError, ValueError) as e:
            conf['UserSettings']['key'] = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
            cipher_suite = Fernet(str.encode(conf['UserSettings']['key']))
        
        plain_text = cipher_suite.decrypt(str.encode(conf['UserSettings']['Password']))
        conf['UserSettings']['Password'] = plain_text.decode()

        return(conf)
