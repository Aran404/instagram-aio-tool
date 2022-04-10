'''
Developed by ! Aran#9999
Redistrubuted by ! Kenny#9999, Jillo#0318
'''

# Imports
import requests
import threading
import random
import os
import sys
from datetime import datetime
from colorama import Fore, init
from fake_useragent import UserAgent

init()

class Comments:    
    def __init__(self, post, account, proxy, message) -> None:
        self.post = post
        self.proxy = proxy
        self.user_agent = UserAgent().random
        self.post_id = self.get_id()
        self.messsage = message
        self.session = requests.Session()
        self.username, self.password = account.split(':')

        if 'Macintosh' in self.user_agent:
            self.os = 'Macintosh'
        elif 'Windows' in self.user_agent:
            self.os = 'Windows'
        elif 'Linux' in self.user_agent:
            self.os = 'Linux'
        else:
            self.os = 'undefined'

    def get_id(self):
        self.create_session()
        get_postid = self.session.get(self.post).content
        return str(get_postid).split('instagram://media?id=')[1].split('"/>')[0]

    def create_session(self):
        self.session.proxies = self.proxy
        
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

        get_acc_data = self.session.post('https://www.instagram.com/accounts/login/ajax/', data={
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{datetime.now().timestamp()}:{self.password}',
            'username': self.username,
            'queryParams': {},
            'optIntoOneTap': False,
            'stopDeletionNonce': None,
            'trustedDeviceRecords': {},
        })

        self.session_id = get_acc_data.headers['set-cookie'].split('sessionid=')[1].split(';')[0]
        self.ds_user_id = get_acc_data.headers['set-cookie'].split('ds_user_id=')[1].split(';')[0]
        self.claim = get_acc_data.headers['x-ig-set-www-claim']

        self.session.cookies['ds_user_id'] = self.ds_user_id
        self.session.cookies['sessionid'] = self.session_id
        self.session.cookies['rur'] = 'NAO'

        self.cookie1 = f'mid={self.mid}; ig_did={self.ig_did}; ig_nrcb={self.ig_nrcb}; csrftoken={self.csrf}; rur=NAO; ds_user_id={self.ds_user_id}; sessionid={self.session_id}'

        self.session.headers.update({'cookie': self.cookie1})

        get_set_cookie = self.session.get('https://www.instagram.com/accounts/onetap/')

        self.shbid = get_set_cookie.headers['set-cookie'].split('shbid=')[1].split(';')[0]
        self.shbts = get_set_cookie.headers['set-cookie'].split('shbts=')[1].split(';')[0]
        self.rur = get_set_cookie.headers['set-cookie'].split('rur=')[1].split(';')[0]

        self.session.cookies['shbid'] = self.shbid
        self.session.cookies['shbts'] = self.shbts
        self.session.cookies['rur'] = self.rur
        
        self.cookie2 = f'mid={self.mid}; ig_did={self.ig_did}; ig_nrcb={self.ig_nrcb}; csrftoken={self.csrf}; rur=NAO; ds_user_id={self.ds_user_id}; sessionid={self.session_id}; shbid={self.shbid}; shbts={self.shbts}; rur={self.rur}'

        self.session.headers.update({'x-ig-www-claim': self.claim})

    def __main__(self):
        comment_post = self.session.post(f'https://www.instagram.com/web/comments/{self.post_id}/add/', data={
            'comment_text': self.messsage,
            'replied_to_comment_id': None
        })
        if comment_post.json()['status'] == 'ok':
            sys.stdout.write(f'{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} Commented on [{self.username}:{self.password}]\n')
            return True
        else:
            sys.stdout.write(f'{Fore.RED}[{Fore.WHITE}-{Fore.RED}]{Fore.WHITE} Could not comment on [{self.username}:{self.password}]\n')
            print(comment_post.json())
            return False

if __name__ == '__main__':
    os.system('cls' if os.name=='nt' else 'clear')

    proxies = open('Proxies.txt','r').read().splitlines()

    if proxies == []:
        proxies = [None]

    accounts = open('Accounts.txt','r').read().splitlines()
    post = input('What post do you want to comment on -> ')
    comment = input('What do you want to comment -> ')

    for account in accounts:
        threading.Thread(target=Comments(post, account, random.choice(proxies), comment).__main__)

