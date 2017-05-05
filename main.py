from imports import * 
from classes import * 
from support import * 
import getpass
from cryptography.fernet import Fernet

warnings.filterwarnings('ignore', category=UserWarning)
CONFIG_SETTINGS = dict(auto_envvar_prefix='config')

pass_config = click.make_pass_decorator(config, ensure=True)

@click.group()
@pass_config
def kl(config):
    """
    A unofficial Kaggle CLI with a few more features
    """
    
@kl.command()
@pass_config
def setup(config):
    """
    Helps setup login details 
    """
    opt = {}
    
    username = input('UserName: ')
    password = getpass.getpass(prompt='Password: ')
    password = str.encode(password)
    
    # need to make sure that config file does not already 
    # exist, and if it does, check its validity.
    #config_file = config.config_file
    #key = str.encode(config_file['key'])
    
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password)
    cipher_text = cipher_text.decode()
    
    opt['key'] = 'hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I='
    opt['UserName'] = username
    opt['Password'] = cipher_text
    opt['action'] = 'login'
    
    with open(config_path, 'w') as f:
        json.dump(opt, f)
    
    print('Done')
    sys.exit()
    
@kl.command()
@click.option('--comp', default=None, type=str, help='Needs a competiton name to download either training or test Set')
@click.option('--tr', default=False, is_flag=True, help='This option downloads training set only')
@click.option('--te', default=False, is_flag=True, help='This option downloads test set only')
@pass_config
def dl(config, comp, tr=False, te=False):
    """
    Downloads competition test or train data, 
    default downloads both (not recommended if time is of essence)
    """
    comp_exists = cexist(config, comp)
    all_competitions = config.comp_file

    if comp_exists:
        print("""Competition Exists...""")
        with requests.Session() as session:
            logged_in = login(config, session, root_url, test_url)
            username = config.config_file['UserName']
            if logged_in:
                print("""Logged in as %s...""" % username)
                comp_url = str(all_competitions[comp][0])
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
                        print("""No training or test option selected. Downloading both...""")
                        
                        print("""Downloading Training set...""")
                        download_url(session, trainingSetUrl)
                        
                        print("""Downloading Training set...""")
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
        print("""
                    No Competition mentioned, the command can be used as 'kl dl --comp <competion name>...'.
                    A list of all competitions can be found by executing 'kl list'
        """)
        return(0)

#@kl.command()
#@pass_config
#def list(config):
#    """
#    Lists all competition names
#    """
#    comp_data = config.comp_load()
#    with open('data/keys.txt', 'w') as f:
#        for key in comp_data.keys():
#            w = key + '\n'
#            f.write(w)
#    subprocess.call(['cat keys.txt | less'], shell=True)


# all below functions are placed in order of execution in main loop (my mind works like that)
# 1. Check if the competition exists
@pass_config
def cexist(config, comp=None): 
    """
    Checks if the given competition exists within the given data set
    """
    if(comp==None):
        print("No competition name given, please try again with the --comp option")
        sys.exit()
    comp_data = config.comp_load()
    if comp in comp_data.keys():
        return(True)
    else:
        return(False)
    
# 3. if logged in, check if competition rules have been accepted by the user
# @pass_config
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
