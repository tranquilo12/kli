# for everything that the command line interface does
import click 

# for accessing websites
import requests 

# for making sure the 'list' command lists all in one page
import subprocess, argparse, argcomplete
from argcomplete.completers import ChoicesCompleter

# for parsing the soups that are thrown out of websites
from bs4 import BeautifulSoup

# for the progressbars 
from tqdm import * 

# for re for matching, sys for system access and time for timing
import re, json, warnings, sys
