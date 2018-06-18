from requestium import Session, Keys
import json
import time
import random
from random import *
import requests

with open("config.json") as file:
    config = json.load(file)

alphabet = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z'
]

def genName():
    string = ""
    for i in range(randint(6, 10)):
        case = randint(0, 1)
        if case == 0:
            ca = alphabet[randint(0, len(alphabet) - 1)]
            string = string + str(ca)
        else:
            ca = randint(0, 9)
            string = string + str(ca)
    return string

def gen(num, limit):
    s = Session(webdriver_path='chromedriver.exe', browser='chrome')
    s.driver.get("https://privacy.com/login")
    time.sleep(3)
    s.driver.find_element_by_xpath('//*[@id="steps"]/div/form/div[2]/label[1]/input').send_keys(config['username'])
    s.driver.find_element_by_xpath('//*[@id="steps"]/div/form/div[2]/label[2]/input').send_keys(config['password'])
    time.sleep(1)
    s.driver.find_element_by_xpath('//*[@id="steps"]/div/form/div[3]/button').click()
    time.sleep(2)
    s.transfer_driver_cookies_to_session()
    s.driver.quit()
    url1 = "https://privacy.com/api/v1/card"

    for i in range(int(num)):
        h1 = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': 'Bearer {}'.format(s.cookies['token']),
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'sessionID={}; ETag="ps26i5unssI="; waitlist_cashback=%7B%22refByCode%22%3A%22favicon.ico%22%2C%22isPromotional%22%3Afalse%7D; landing_page=extension-rewards-landing; token={}'.format(s.cookies['sessionID'], s.cookies['token']),
            'Host': 'privacy.com',
            'Origin': 'https://privacy.com',
            'Pragma': 'no-cache',
            'Referer': 'https://privacy.com/home',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }

        pay = {
            "type":"MERCHANT_LOCKED",
            "spendLimitDuration":"MONTHLY",
            "memo":genName(),
            "meta":{
                "hostname":""
            },
            "style":'null',
            "spendLimit":int(limit),
            "reloadable":'true'
        }

        r = s.post(url1, json=pay, headers=h1)

        if r.status_code == requests.codes.ok:
            print("[{}] !~Created Card~!".format(r.json()['card']['cardID']))
            with open("cards.txt", "a+") as file:
                file.write("{}:{}/{}:{}\n".format(r.json()['card']['pan'], r.json()['card']['expMonth'], r.json()['card']['expYear'], r.json()['card']['cvv']))
        else:
            print("Error Creating Card")




if __name__ == '__main__':
    print("Privacy Card Gen v2")
    print("https://github.com/TCWTEAM/privacy-card-gen-v2")
    num = input("# Of Cards To Gen: ")
    lim = input("Limit On Cards (e.x 30): ")
    gen(num, lim)
