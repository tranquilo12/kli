from imports import * 
from cryptography.fernet import Fernet

root_url = 'https://www.kaggle.com'
login_url = '/account/login'
test_url = '/c/titanic'
rules = '/rules'
data = '/data'

config_path = click.get_app_dir('kl') + '/config.json'
comp_path = 'data/comp.json'

class config(object):
    def __init__(self, *args, **kwargs): 
        self.config_filepath = config_path
        self.config_file = self.config_load()

        self.comp_filepath = comp_path
        self.comp_file = self.comp_load()
        super(config, self).__init__()

    def config_load(self):
        with open(self.config_filepath, 'r') as f:
            try:
                d = json.load(f)
            except (ValueError, KeyError) as e:
                    opt = {}
                    key = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
                    opt['key'] = key
                    opt['Password'] = 'gAAAAABZC018YC8y4q9gdnI-xIuNXeySuP-hOIqkqTkKxAiSQOZvGPToU8wan6_xgm8bXk-KdrBdJjsdhGOnDv1PC5ipU5FbqQ=='
                    opt['UserName'] = 'UserName'
                    opt['action'] = 'login'
                    
                    with open(self.config_filepath, 'w') as fp:
                        json.dump(opt, fp)
                        
                    print("""
                    The config_file was restored to default (or a new config_file was just made). 
                    You can reset your settings via the command 'kl setup'.
                    """)
                    
                    with open(self.config_filepath, 'r') as fp: 
                        d = json.load(fp)
                    
            try: 
                cipher_suite = Fernet(str.encode(d['key']))
            except KeyError: 
                d['key'] = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
                cipher_suite = Fernet(str.encode(d['key']))
                
            plain_text = cipher_suite.decrypt(str.encode(d['Password']))
            d['Password'] = plain_text
            return(d)

    def comp_load(self):
        with open(self.comp_filepath) as f:
            d = json.load(f)
            return(d)
