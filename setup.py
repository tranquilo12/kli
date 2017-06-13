from setuptools import setup, find_packages

setup(
    name = 'kli', 
    version = '0.0.15', 
    packages = find_packages(exclude=['venv', 'backup']),
    license = 'MIT',
    url = 'https://github.com/tranquilo12/kli',
    author = 'Shriram Sunder',
    author_email = 'shriram.sunder121091@gmail.com',
    install_requires = [
        'tqdm', 
        'pprint',
        'argcomplete',
        'bs4', 
        'click>=6', 
        'cryptography', 
        'requests',
        'lxml',
        ],    
    entry_points = '''
        [console_scripts]
        kli=kli.main:kli
    ''',
    keywords = ['kaggle', 'cli'],
    #data_files=[('data', ['comp.json']),
    #            ('data', ['keys.txt'])]
        )
