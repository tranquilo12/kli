# for everything that the command line interface does
import click 

# for accessing websites
import requests 

# for parsing the soups that are thrown out of websites
from bs4 import BeautifulSoup

# for the progressbars 
from tqdm import * 

# for re for matching, sys for system access, warnings to supresses some warnings, 
# and os for making/reading files/dirs
import re, json, warnings, sys, os

# for password input, and crypto
import getpass
from cryptography.fernet import Fernet
import configparser