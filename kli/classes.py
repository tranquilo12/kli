from .imports import * 

root_url = 'https://www.kaggle.com'
login_url = '/account/login'
test_url = '/c/titanic'
rules = '/rules'
data = '/data'


class config(object):

    config_filepath = click.get_app_dir('kli') + '/kli.ini'

    def __int__(self, *args, **kwargs): 
        #self.config_filepath = config_filepath
        # if the file location doesnt exist
        if not os.path.isfile(self.config_filepath):
            os.makedirs(click.get_app_dir('kli'), exist_ok=True)
            print("\nMaking new config file...\n")
            self.config_write()
        # if the conf file does exit, check its integrity
        else:
            if os.stat(self.config_filepath).st_size == 0:
                print("""\nThe current config file seems to be currupted. 
Please run the command 'kli make' to make a new config file.\n""")
            else:
                # if the config file exists, and is valid
                try:
                    self.config_file = self.config_read()
                except ValueError:
                    print("\nError retrieving conf file, try deleting it and then running the command 'kli make'.\n")
        super(config, self).__init__()
    
    def config_write(self):
        conf = configparser.ConfigParser()
        conf.optionxform = str
        conf.add_section('UserSettings')
        key = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
        conf['UserSettings']['key'] = key
        with open(self.config_filepath, 'w') as f: 
            conf.write(f)
        print("""\nThe config file was restored to its default value (or a new config file was made). 
You can reset your user settings via the command 'kl setup'.\n""")

    def config_read(self):
        if not os.path.isfile(self.config_filepath):
            print("\nConfig file not found in %s \n" %config_path)
            print("""\nYou can make an empty config file in the above location, or
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
        
        try:
            plain_text = cipher_suite.decrypt(str.encode(conf['UserSettings']['Password']))
            conf['UserSettings']['Password'] = plain_text.decode()
        except KeyError: 
            print("There was an error, please try 'kli setup' to refresh the config file.")

        return(conf)
