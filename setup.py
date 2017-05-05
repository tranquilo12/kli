from setuptools import setup, find_packages

setup(
    name = 'kl', 
    version = '0.0.1', 
    packages = find_packages(exclude=['venv', 'backup']),
    license = 'MIT',
    url = '',
    author = 'Shriram Sunder',
    author_email = 'shriram.sunder121091@gmail.com',
    install_requires = [
        'tqdm', 
        'pprint',
        'argcomplete',
        'bs4', 
        'click>=6', 
        'cryptography'
        ],    
    entry_points = '''
        [console_scripts]
        kl=main:kl
    ''',
    data_files=[('data', ['comp.json']),
                ('data', ['keys.txt'])]
        )
