# Imports
from selenium_stealth import stealth
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from colorama import Fore, init
import string
import time
import random
import requests
import os


class Phone:
    def __init__(self, api_key, phone_id) -> None:
        self.api_key = api_key
        self.phone_id = phone_id

    def get_number(self) -> dict:
        token = self.api_key
        country = "russia"
        operator = "any"
        product = "instagram"

        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        }

        response = requests.get(
            "https://5sim.net/v1/user/buy/activation/"
            + country
            + "/"
            + operator
            + "/"
            + product,
            headers=headers,
        ).json()

        return {
            "number": response["phone"],
            "phone_id": response["id"],
            "price": response["price"],
        }

    def get_balance(self) -> int:
        token = self.api_key

        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        }

        return int(
            round(
                requests.get(
                    "https://5sim.net/v1/user/profile", headers=headers
                ).json()["balance"],
                3,
            )
        )

    def get_code(self):
        token = self.api_key
        c_id = self.phone_id

        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        }

        tries = 0
        while tries < 30:
            response = requests.get(
                "https://5sim.net/v1/user/check/" + str(c_id), headers=headers
            ).json()
            if response["status"] == "RECEIVED":
                if response["sms"]:
                    return response["sms"][0]["code"]
            else:
                time.sleep(2)
                tries += 1

        return False

    def finish_order(self) -> None:
        token = self.api_key
        c_id = self.phone_id

        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        }

        requests.get("https://5sim.net/v1/user/finish/" + str(c_id), headers=headers)

    def cancel_order(self) -> None:
        token = self.api_key
        c_id = self.phone_id

        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        }

        requests.get("https://5sim.net/v1/user/cancel/" + str(c_id), headers=headers)


class Generator:
    def __init__(self, proxy, api_key) -> None:
        self.proxy = proxy
        self.api_key = api_key

        self.useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

        self.username = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(10)
        )

        self.fname = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(6)
        )

        self.password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(10)
        )

    def __init_driver__(self) -> None:
        ser = Service(f"{os.getcwd()}\chromedriver.exe")
        proxy_server = self.proxy

        if proxy_server == False:
            capabilities = None
        else:
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxy_server
            proxy.ssl_proxy = proxy_server
            capabilities = webdriver.DesiredCapabilities.CHROME
            proxy.add_to_capabilities(capabilities)

        # Spoofing to not get detected
        options = Options()

        options.add_experimental_option(
            "excludeSwitches",
            [
                "enable-logging",
                "enable-automation",
                "ignore-certificate-errors",
                "safebrowsing-disable-download-protection",
                "safebrowsing-disable-auto-update",
                "disable-client-side-phishing-detection",
            ],
        )

        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--lang=en")
        options.add_argument("--log-level=3")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--profile-directory=Null")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={self.useragent}")
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(
            service=ser, desired_capabilities=capabilities, options=options
        )

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.driver.set_window_size(500, 570)

        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": self.useragent}
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
            Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 99
            })
        """
            },
        )

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
            },
        )

    def get_dob(self) -> dict:
        month = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "Decemeber",
        ]

        return {
            "year": random.randint(1970, 2000),
            "month": random.choice(month),
            "day": random.randint(1, 27),
        }

    def __main__(self) -> None:
        self.__init_driver__()
        self.driver.get("https://www.instagram.com/accounts/emailsignup/")

        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='emailOrPhone']",
                )
            )
        )

        get_phone = Phone(self.api_key, None).get_number()
        self.phone_num, self.phone_id = get_phone["number"], get_phone["phone_id"]

        for char in self.phone_num:
            self.driver.find_element(
                By.XPATH, "//input[@name='emailOrPhone']"
            ).send_keys(char)
            time.sleep(random.uniform(0.32, 0.62))

        for char in self.fname:
            self.driver.find_element(By.XPATH, "//input[@name='fullName']").send_keys(
                char
            )
            time.sleep(random.uniform(0.32, 0.62))

        for char in self.username:
            self.driver.find_element(By.XPATH, "//input[@name='username']").send_keys(
                char
            )
            time.sleep(random.uniform(0.32, 0.62))

        for char in self.password:
            self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(
                char
            )
            time.sleep(random.uniform(0.32, 0.62))

        WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[type='submit']",
                )
            )
        )

        time.sleep(random.uniform(1.1, 1.4))

        self.driver.execute_script(
            """
            document.querySelector("button[type='submit']").click();
        """
        )

        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//select[@title='Month:']",
                )
            )
        )

        Select(
            self.driver.find_element(By.XPATH, "//select[@title='Month:']")
        ).select_by_visible_text(str(self.get_dob()["month"]))
        time.sleep(random.uniform(1.1, 1.2))
        Select(
            self.driver.find_element(By.XPATH, "//select[@title='Day:']")
        ).select_by_visible_text(str(self.get_dob()["day"]))
        time.sleep(random.uniform(1.1, 1.2))
        Select(
            self.driver.find_element(By.XPATH, "//select[@title='Year:']")
        ).select_by_visible_text(str(self.get_dob()["year"]))
        time.sleep(random.uniform(1.1, 1.2))

        WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Next']",
                )
            )
        )

        time.sleep(random.uniform(1.1, 1.2))
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()

        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='confirmationCode']",
                )
            )
        )

        self.sms_code = Phone(self.api_key, self.phone_id).get_code()
        if self.sms_code is False:
            return

        for char in str(self.sms_code).strip():
            self.driver.find_element(
                By.XPATH, "//input[@name='confirmationCode']"
            ).send_keys(char)
            time.sleep(random.uniform(0.34, 0.56))

        time.sleep(random.uniform(1.1, 1.2))
        self.driver.execute_script(
            """
            document.querySelector("form[method='POST'] button[type='button']").click();
        """
        )

        with open("accounts.txt", "a") as accounts:
            accounts.write(f"{self.username}:{self.password}")

        time.sleep(10)

        self.driver.quit()


os.system("cls" if os.name == "nt" else "clear")
Generator(
    "PROXY",
    "5sim API KEY",
).__main__()
