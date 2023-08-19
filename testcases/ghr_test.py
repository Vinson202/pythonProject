import json

import requests

# 获取GA WEB的登录token
from bs4 import BeautifulSoup


def get_gaweb_token(idpUser,idp_cred):
    S = requests.session()
    S.keep_alive = False
    loginurl = "https://api-b2b-qa.cn-pgcloud.com/paas-ssofed/v3/login?"
    loginparams = {"pfidpadapterid": "ad..OAuth",
                   "app": "GhrGAWeb",
                   "subscription-key": "2787a94d8fe9405fbccde0160a85c591"}
    html1 = S.get(loginurl, params=loginparams)
    # print(html1.url)
    # print(html1.content)
    url2 = html1.url
    headers2 = {"Referer": "https://qa-ga-webportal.pg.com.cn/"}
    html2 = S.get(url2, headers=headers2)
    cookies = html1.cookies.get_dict()
    loginBody = html1.content
    pingdata = BeautifulSoup(loginBody, 'html.parser')
    action = pingdata.form.attrs['action']
    # print(action)
    domain = str(pingdata.base.attrs['href']).rstrip('/')
    url = domain + action
    pf_adapterId = pingdata.find(attrs={'name': 'pf.adapterId'}).get('value')
    # print(url)
    data = {
        "pf.username": idpUser,  # "wei.ws.7",
        "pf.pass": idp_cred,  # "Gdnchina2",
        "pf.ok": "clicked",
        "pf.adapterId": pf_adapterId
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Host": "fedauth.pg.com.cn",
        "Origin": "https://fedauth.pg.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://fedauth.pg.com.cn/",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
    }
    html2 = S.post(url, headers=headers, data=data, allow_redirects=True)
    # print("html2: ", html2.url)
    code = html2.url.split('code=')[1]
    # print("code: ", code)
    url2 = "https://qa-ga-webportal.pg.com.cn/api/v1/ga/console/gaweb/sso/auth?authCode=" + code

    headers2 = {"Referer": "https://qa-ga-webportal.pg.com.cn/login",
                "Host": "qa-ga-webportal.pg.com.cn",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
                }
    html3 = S.get(url2, headers=headers2)
    return 'Bearer {}'.format(json.loads(html3.content)['token'])
    # token = 'Bearer {}'.format(json.loads(html3.content)['token'])
    print(token)
    return token


print(get_gaweb_token('wei.ws.7', 'Ht1pailRinfox#gKs9M:2'))