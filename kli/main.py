from .imports import * 
from .classes import * 
from .support import * 
import getpass
from cryptography.fernet import Fernet

warnings.filterwarnings('ignore', category=UserWarning)
CONFIG_SETTINGS = dict(auto_envvar_prefix='config')

pass_config = click.make_pass_decorator(config, ensure=True)

@click.group()
@pass_config
def kli(config):
    """
    A unofficial Kaggle CLI with a few more features
    """

@kli.command()
@pass_config
def setup(config):
    """
    Helps setup login details.
    """
    username = input('UserName: ')
    password = getpass.getpass(prompt='Password: ')
    password = str.encode(password)
    
    if not os.path.isfile(config.config_filepath): 
        print("\nConfig file not found in %s \n" %config_path)
        print("""You can make an empty config file in the above location, or
run the command 'kli mconfig', which will make one for you.\n""")
        sys.exit(0)

    # dont make the file, that's kli mconfig's resposibility
    # assume the file is present, and replace with the users settings

    conf = configparser.ConfigParser()
    conf.read(config.config_filepath)
    conf.optionxform = str
   
    key = conf['UserSettings']['key']
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password)
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
def mconfig(config):
    """
    Makes config file, if one doesn't exist.
    """
    #check if the file exists, 
    #and ask user to reset config instead 
    if os.path.isfile(config.config_filepath): 
        print("A config file already exists, 'kli setup' will reset your user settings instead.")
    else:
        print("Making new config file for user.")
        config.make_config()
        print("Done.")

@kli.command()
@click.option('--comp', default=None, type=str, help='Need competiton url to download data')
@click.option('--tr', default=False, is_flag=True, help='This option downloads training set only')
@click.option('--te', default=False, is_flag=True, help='This option downloads test set only')
@pass_config
def dl(config, comp, tr=False, te=False):
    """
    Downloads competition test or train data, 
    default downloads both (not recommended if time/space is of essence)
    """
    #check for comp validity
    comp = check_comp(comp)

    if comp != None:
        print("""Competition Url Valid...""")
        with requests.Session() as session:
            logged_in = login(config, session, root_url, test_url)
            username = config.config_file['UserName']
            if logged_in:
                print("""Logged in as %s...""" % username)
                comp_url = comp
                rules_accepted = crules(session, root_url, comp_url, rules)
                if rules_accepted:
                    print("""Rules accepted...""")
                    data_response = session.get(root_url + comp_url + '/data') 
                    soup = BeautifulSoup(data_response.text, 'lxml')
                    testSetUrl, trainingSetUrl = get_links(soup, all_competitions[comp][0][3::])
                    if te:
                        print("""Downloading Test set...""")
                        download_url(session, testSetUrl)
                        sys.exit()
                    if tr:
                        print("""Downloading Training set...""")
                        download_url(session, trainingSetUrl)
                        sys.exit()
                    if tr==False and te==False:
                        print("""No --tr or --te option selected. Downloading all...""")
                        print("""Downloading Training set...""")
                        download_url(session, trainingSetUrl)
                        print("""Downloading Test set...""")
                        download_url(session, testSetUrl)
                else:
                    print("""
                    An Error occured whilst retrieving the page. 
                    Perhaps the rules for this competion have not been accepted. 
                    The rules can be accepted here %s
                    """ % (root_url + comp_url + rules) )
            else:
                print("""
                    Not logged in, perhaps due to an error in your username/password.
                    You can overwrite your current user settings via the command 'kl setup'.
                        """)
                return(0)
    else:
        print("""No Competition Url given, please try again using the command 'kl dl --comp <competion name>...' """)
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
def crules(session, root_url, comp_url, rules):
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
    
