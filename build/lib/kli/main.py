from .classes import * 

warnings.filterwarnings('ignore', category=UserWarning)
CONFIG_SETTINGS = dict(auto_envvar_prefix='config')

pass_config = click.make_pass_decorator(config, ensure=True)

@click.group()
@pass_config
def kli(config):
    """
    An unofficial Kaggle CLI (with a conf file)
    """

@kli.command()
@pass_config
def setup(config):
    """
    Helps setup login details.
    """
    username = input('UserName: ')
    password = getpass.getpass(prompt='Password: ')
    
    if not os.path.isfile(config.config_filepath): 
        print("\nConfig file not found in %s \n" %config_path)
        print("""You can make an empty config file in the above location, or
run the command 'kli mconfig', which will make one for you.\n""")
        sys.exit(0)

    # dont make the file, that's kli mconfig's resposibility
    # assume the file is present, and replace with the users settings

    conf = configparser.ConfigParser()
    try:
        conf.read(config.config_filepath)
    except configparser.DuplicateOptionError:
        print("A naming conflit has occured in the conf file. Please delete it, and try the commands 'kli make', and 'kli setup' to refresh the file.")
        sys.exit(0)
        
    conf.optionxform = str
    
    key = conf['UserSettings']['key']
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(str.encode(password))
    cipher_text = cipher_text.decode()
    
    conf['UserSettings']['key'] = key
    conf['UserSettings']['Password'] =  cipher_text
    conf['UserSettings']['UserName'] =  username
    conf['UserSettings']['action'] = 'login'

    with open(config.config_filepath, 'w') as f: 
        conf.write(f)
    
    print('Done')
    return(0)

@kli.command()
@pass_config
def make(config):
    """
    Makes config file, if one doesn't exist.
    """
    #check if the file exists, 
    #and ask user to reset config instead 
    if os.path.isfile(config.config_filepath): 
        print("A config file already exists, 'kli setup' will reset your user settings instead.")
    else:
        print("Making new config file for user.")
        config.config_write()
        print("Done.")

@kli.command()
@click.option('--comp', default=None, type=str, help='Need competiton url to download data')
@pass_config
def dl(config, comp):
    """
    Downloads competition test or train data, 
    default downloads both (not recommended if time/space is of essence)
    """
    #check if config file exists

    #check for comp validity
    comp = check_comp(comp)

    if comp != None:
        print("""Competition Url Valid...""")
        with requests.Session() as session:
            logged_in = login(config, session, root_url, test_url)
            config_file = config.config_read()
            username = config_file['UserSettings']['UserName']
            if logged_in:
                print("""Logged in as %s...""" % username)
                comp_url = comp
                rules_accepted = check_rules(session, root_url, comp_url, rules)
                if rules_accepted:
                    print("""Rules accepted...""")
                    data_response = session.get(root_url + comp_url + '/data') 
                    soup = BeautifulSoup(data_response.text, 'lxml')
                    #get the comp's name from the url (without /c/)
                    comp_name = comp_url[3:]
                    links = re.findall('"url":"(/c/{}/download/[^"]+)"'.format(comp_name), str(soup))
                    print("""Files awailable for download: """)
                    for link in links:
                        print(link)
                        
                    print("""Which would you like to download? Your answer should be like: 1,2,3""")
                    options = input("Options: ")
                    # check integrity of options
                    if len(options) == 0:
                        print('No option provided, please try again with valid options.')
                        sys.exit(0)
                    for s in options.split(','): 
                        if not s.isdigit(): 
                            print('Invalid option(s). Please provide digits only.')
                            sys.exit(0)
                    # download if integrety is fine
                    for o in map(int, options.split(',')):
                        print("""Downloading %s"""%links[o-1])
                        download_url(session, root_url + links[o-1])
                # if the rules were not accepted
                else:
                    print("""An Error occured whilst retrieving the page. 
Perhaps the rules for this competion have not been accepted. 
The rules can be accepted here %s""" % (root_url + comp_url + rules))
            # If not logged in
            else:
                print("""Not logged in, perhaps due to an error in your username/password.
You can overwrite your current user settings via the command 'kli setup'.""")
                return(0)
    # if the competition url is not clean
    else:
        print("""No Competition Url given, please try again using the command 'kli dl --comp <competion url>' """)
        return(0)

# All below functions are placed in order of execution in main loop (my mind works like that)
# Checks if the given competition url is properly formatted
def check_comp(comp=None): 
    """
    Checks if the given competition url is properly formatted
    """
    if(comp==None):
        return(None)
    if comp.endswith('/'): 
        comp = comp[:-1]
    if comp.startswith('/'): 
        pass
    else: 
        comp = '/' + comp 
    return(comp)

# 3. if logged in, check if competition rules have been accepted by the user
def check_rules(session, root_url, comp_url, rules):
    """
    Checks if competition rules have been accepted
    """
    response = session.get(root_url + comp_url + rules)
    soup = BeautifulSoup(response.text, 'lxml')
    hasAcceptedRules = re.findall('"hasAcceptedRules":(\w+)', str(soup))
    if hasAcceptedRules[0]=='true':
        return(True)
    else:
        return(False) 
    
# was in support.py, now in main    
# 2. if it exists, login
def login(config, session, root_url, test_url):
    """
    Check if the function has logged in, 
    calls another function, which checks username once logged 
    in, to ensure login and login of the right account
    """
    # may have to later change this to email or something 
    # more innocuous
    # need to login first 
    username = ['']
    login_data = config.config_read()
    
    login_data = {
    "UserName":("%s"%login_data['UserSettings']['UserName']),
    "Password":("%s"%login_data['UserSettings']['Password']),
    "action":"Login",
    }
    
    session.post(root_url + login_url, data=login_data)
    response = session.get(root_url + test_url)
    soup = BeautifulSoup(response.text, 'lxml')
    username = re.findall('"user_name": "(\w+)"', str(soup))
    
    try:
        if username[0] == '' or username[0] == None:
            return(False)
        if username[0] == login_data['UserName']:
            return(True)
    except IndexError:
        return(False)

# 5. if rules are accepted, according to the flag passed, the file is downloaded
def download_url(session, url):
    """
    Downloads test or train file: 
    extracts name from url,
    uses tqdm progressbar
    """ 
    response = session.get(url, stream=True)
    content_type = response.headers.get('Content-Type')
    
    total_length = int(response.headers.get('Content-Length'))
    
    filename = re.compile('[^/]+$').search(url).group(0)
    
    with open(filename, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), 
                        total=total_length/1024, 
                        unit='KB'):
            f.write(chunk)
    
    print('Done')
