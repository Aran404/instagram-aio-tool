'''
Developed by ! Aran#9999
Redistrubuted by ! Kenny#9999, Jillo#0318
'''

# Imports
import string
import requests
import threading
import os
import time
import random
from fake_useragent import UserAgent
from datetime import datetime

# Kopeechka
class Email:
    def __init__(self, api_key, domain, id) -> None:
        self.api_key = api_key
        self.domain = domain
        self.email_id = id

    def get_email(self):
        get_mail = requests.get(f'https://api.kopeechka.store/mailbox-get-email?api=2.0&spa=1&site=instagram.com&sender=instagram&regex=&mail_type={self.domain}&token={self.api_key}').json()
        if get_mail['status'] == 'OK':
            return {'mail': get_mail['mail'], 'id': get_mail['id']}
        else:
            return get_mail['value']

    # This part was taken from Hattorius
    def checkEmail(self):
        return requests.get('https://api.kopeechka.store/mailbox-get-message?full=1&spa=1&id=' + self.email_id + '&token=' + self.api_key).json()['value']

    def deleteEmail(self):
        requests.get('https://api.kopeechka.store/mailbox-cancel?id=' + self.email_id + '&token=' + self.api_key)

    def waitForEmail(self):
        tries = 0
        while tries < 30:
            time.sleep(2)
            value = self.checkEmail(self.email_id)
            if value != 'WAIT_LINK':
                self.deleteEmail(self.email_id)
                return value.replace('\\', '')
            tries += 1
        return False

class Creation:
    def __init__(self, proxy, email, email_id) -> None:
        self.session = requests.Session()
        self.user_agent = UserAgent().random
        self.email = email
        self.email_id = email_id
        self.proxy = proxy

    def get_dob(self):
        month = {
            '1': 'January',
            '2': 'February',
            '3': 'March',
            '4': 'April',
            '5': 'May',
            '6': 'June',
            '7': 'July',
            '8': 'August',
            '9': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'Decemeber'
        }
        num = random.randint(1,12)

        return {'year': random.randint(1970,2000), 'month': month[str(num)], 'day': random.randint(1,27)}

    def create_headers(self):
        self.proxy = 'a proxy'
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

        request_data = self.session.get('https://www.instagram.com/accounts/emailsignup/', timeout=30)
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

    def create_account(self):
        self.create_headers()
        username = "".join(random.choice(string.ascii_letters + string.digits) for x in range(10))
        first_name = "".join(random.choice(string.ascii_letters) for x in range(10))

        _ = self.session.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', data={
            'email': self.email,
            'username': None,
            'first_name': None,
            'opt_into_one_tap': False
        })

        __ = self.session.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', data={
            'email': self.email,
            'username': username,
            'first_name': None,
            'opt_into_one_tap': False
        })

        ___ = self.session.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', data={
            'email': self.email,
            'username': username,
            'first_name': first_name,
            'opt_into_one_tap': False
        })

        ____ = self.session.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', data={
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:Ethanisnotcool123',
            'email': self.email,
            'username': username,
            'first_name': first_name,
            'client_id': self.mid,
            'seamless_login_enabled': 1,
            'opt_into_one_tap': False,
        }, timeout=30)

        day, month, year = str(self.get_dob()['day']), str(self.get_dob()['month']), str(self.get_dob()['year'])

        _____ = self.session.post('https://www.instagram.com/web/consent/check_age_eligibility/', data={
            'day': day,
            'month': month,
            'year': year
        })

        ______ = self.session.post('https://i.instagram.com/api/v1/accounts/send_verify_email/', data={
            'device_id': self.mid,
            'email': self.email
        })

        global api_key
        code = Email(api_key, None, self.email_id).waitForEmail()

        _______ = self.session.post('https://i.instagram.com/api/v1/accounts/check_confirmation_code/', data={
            'code': code,
            'device_id': self.mid,
            'email': self.email
        })

        sign_up_code = _______.json()['signup_code']

        _________ = self.session.post('https://www.instagram.com/accounts/web_create_ajax/', data={
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:Ethanisnotcool123',
            'email': self.email,
            'username': username,
            'first_name': first_name,
            'month': month,
            'day': day,
            'year': year,
            'client_id': self.mid,
            'seamless_login_enabled': 1,
            'tos_version': 'row',
            'force_sign_up_code': sign_up_code,
        })

        if _________.json()['message'] == '':
            return False
        else:
            with open('Accounts.txt','a') as accounts:
                accounts.write(self.email)

if __name__ == '__main__':
    os.system('cls' if os.name=='nt' else 'clear')

    proxies = open('Proxies.txt','r').read().splitlines()

    if proxies == []:
        proxies = [None]

    api_key = input('What is your email api key -> ')
    domain = input('What is the domain you want to use for emails -> ')
    amt_of_acc = int(input('How many accounts do you want to make -> '))
    
    for x in range(amt_of_acc):
        init_email = Email(api_key, domain, None).get_email()
        email = init_email['mail']
        email_id = init_email['id']

        threading.Thread(target=Creation(random.choice(proxies), email, email_id).create_account)
