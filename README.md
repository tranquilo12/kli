# Kaggle-Cli (kli)
Powered by [Click](http://click.pocoo.org/5)

**kli** is an unoffical Kaggle-Cli which helps you avoid entering your username and password repeatedly when downloading a data file from kaggle.

## Installation:
Within your virtual environment:
```sh
$ pip install kli 
```

## Commands: 
- **kli** has 3 commands: make, setup & download.
- **make** makes a ".ini" file which stores your kaggle login credentials.
- **setup** helps you write/overwrite your ".ini" file with your username and password.
- **dl** downloads the files from the competition that you have specified. You have the option of choosing which files to 
download as well.

### Make a Config file
```sh
$ kli make  
```
- This will make a config file in the location **~/.config/kli/kli.ini**.
- If the above command returns a **FileNotFoundError** , make a **kli** directory in **~/.config/** 
and try the command again. 

### Setup a Config file
```sh
$ kli setup  
```
- This will ask you for your kaggle username (**not** email) and password, which will be used to log into your kaggle account.
- The password is encrypted with cryptography's Fernet module to trip OTS attacks **ONLY**.
- Any **FileNotFoundError**'s you face can be solved by the **kli make** command. As it is usually because the cli cannot find the file in the appropriate location  **~/.config/kli/kli.ini**. 

The file (**kli.ini** ) looks like this :
```
[UserSettings]
key = hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I=
Password = gAFRVABNN8P5rwfu1pKzLVf8VosefGIGm9RhvWbTrSLysPBCqzWWJn0ylMUVwlMathkfWJjkkXEh1mHL4rZcUl2Vz7n_Fo9IdjA==
UserName = username223
action = login
```
- The **key**  is used to obsfucate your **Password** to trip OTS attacks only. It is ***not*** meant to protect the file from anything else.
- The **key** can always be replaced, make sure that it is replaced by a key generated via cryptography.fernet.Fernet.generate_key().
- Any errors that you face ( if you change the **key** ) will mostly be related to byte/string encoding/decoding issues, so please be careful whilst changing keys.

### Download Competition files
```sh
$ kli dl --comp <competiton url>
```
- **competiton url** should be of the format `/c/competition_name`
- The command checks if that user has logged into their account & if the user's account has accepted that particular competition's rules.
- If you are not logged in, the cli will exit, and prompt you to setup your ".ini" file again.
- If you have not accepted the rules, please do so through the browser, that feature will not be added to this cli.
- The command also provides you the list of all available files to download, simply enter the number of the file that you wish to download.
- Multiple files can be downloaded by seperating the numbers with a comma.
