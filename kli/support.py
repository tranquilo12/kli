from .imports import * 
from .classes import * 
import json

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
    
    if username[0] == '' or username[0] == None:
        return(False)
    if username[0] == login_data['UserName']:
        return(True)

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
