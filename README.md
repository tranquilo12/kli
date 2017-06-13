# Kaggle-CLI (kli)
Powered by [Click](http://click.pocoo.org/5)

Another unoffical Kaggle-CLI

## Installation:
Within your virtual environment:
```sh
$ pip install kli 
```

## Commands: 
**kli** avoids entering your username and password when you decide to download a file from kaggle.

### Make a Config file
```sh
$ kli make  
```

- This will make a config file in the location **~/.config/kli/kli.ini**.
- If the above command returns a **FileNotFoundError** , make a **kli** directory in **~/.config/** 
and try the command again. 

### Setup the Config file
```sh
$ kli setup  
```

- This will ask you for your kaggle username (**not** email) and password, which will be used to log into your kaggle account.
- The password is encrypted with cryptography's Fernet module to trip OTS attacks **ONLY**.
- Any **FileNotFoundError**'s you face can be solved by the **kli make** command. 

The file ( kli.ini ) looks like this :
```
[UserSettings]
key = hpm3j6mDfpL9yMEOkLwMSC2Qwa2jKyEnGeI08yNcv1I=
Password = gAFRVABNN8P5rwfu1pKzLVf8VosefGIGm9RhvWbTrSLysPBCqzWWJn0ylMUVwlMathkfWJjkkXEh1mHL4rZcUl2Vz7n_Fo9IdjA==
UserName = username223
action = login
```

- The **key** :
-- is used to obsfucate your **Password** to trip OTS attacks only. It is ***not*** meant to prevent any other attacks.
-- can always be replaced, make sure that it is generated via cryptography.fernet.Fernet.generate_key().
- Any errors that you face ( if you change the **key** ) will mostly be related to byte/string encoding/decoding issues.  

### Download Competition files
```sh
$ kli dl --comp <competiton url>
```
- <competiton url> follows the format `/c/competition_name`
- The command performs the following important checks:
-- If that user has logged into their account.
-- If the user's account has accepted that particular competition's rules
- The command also provides you with options of all the files to download.