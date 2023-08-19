import json
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import time

from datetime import datetime,timedelta


# 2、获取ISA的token
def get_gaapp_token(idpUser, idp_cred):
    S = requests.session()
    S.keep_alive = False
    loginurl = "https://authtst.cn-pgcloud.com/login"
    html = S.get(loginurl)
    # print(html4.content)
    content = str(html.content)
    # startint = int(content.find('"X-CSRF-TOKEN" content=')) + 24
    # endint = startint + 36
    # CSR = content[startint:endint]
    CSR = re.findall('"X-CSRF-TOKEN" content="(.*?)"', content)[0]
    # print(startint)
    # print(endint)
    # print(content[startint:endint])
    url = "https://authtst.cn-pgcloud.com/signin"
    headers = {"Host": "authtst.cn-pgcloud.com",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Referer": "https://authtst.cn-pgcloud.com/login",
               "Origin": "https://authtst.cn-pgcloud.com"}
    url2 = "https://authtst.cn-pgcloud.com/oauth/authorize?response_type=code&scope=read&client_id=c001c871fe1392479de9ffd8f7bb9886YymxzesZTUW&redirect_uri=https%3A%2F%2Fgoldenambassador-qa.pg.com.cn"
    loginparams = {
        "_enterprise_id": "pg",
        "_csrf": CSR,
        "loginRedirectUrl": url2,
        "idpUser": idpUser,  # 13683221270
        "idp_cred": idp_cred  # "New201907"
    }
    html1 = S.post(url, headers=headers, data=loginparams, allow_redirects=True)
    code = html1.url.split('code=')[1]
    # print(code)
    ghr_url = "https://goldenambassador-qa.pg.com.cn/idp/login?code=" + code
    html3 = S.get(html1.url, allow_redirects=True)
    html4 = S.post(ghr_url, allow_redirects=True)
    # print(html4.content)
    return 'Bearer' + ' ' + json.loads(html4.content)['token']


# print(get_gaapp_token('13812345678', 'New201907'))


# 3、获取gaweb的token
def get_gaweb_token(idpUser, idp_cred):
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


print(get_gaweb_token('wei.ws.7','Ht1pailRinfox#gKs9M:2'))

def get_time():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return timestamp

# print(get_time())

def get_month():
    timestamp = time.strftime('%Y-%m', time.localtime(time.time()))
    return timestamp
# print(get_month())


def get_check_month():
    timestamp = time.strftime('%Y-%m', time.localtime(time.time()))
    return timestamp


def get_work_month():
    timestamp = time.strftime('%Y%m', time.localtime(time.time()))
    return timestamp


def now_data():
    timestamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return timestamp

def tomorrowTime():
    timestamp = datetime.now()+datetime.timedelta(days=1).strftime('%Y-%m-%d')
    return timestamp


# 获取明天
def get_day(n):
    today = datetime.date.today()
    day = (today + datetime.timedelta(n)).strftime("%Y-%m-%d")
    return day

# 获取当前月份的第一天
def first_day_of_month():
    timestamp = datetime(now.year, now.month, 1)
    return timestamp
# print(first_day_of_month())


def get_ghweb_token(loginname, Password):
    S = requests.session()
    url = "https://uat-gh-webportal.pg.com.cn/Account/login?RequestPath=%2F"
    response = S.get(url=url)
    # 获取页面内容：RequestVerificationToken
    content = str(response.content)
    # startint = int(content.find('"__RequestVerificationToken" type="hidden" value="')) + 50
    # endint = startint + 155
    # RequestVerificationToken = re.findall('"__RequestVerificationToken" type="hidden" value="(.*?)"', content)[0]
    # print(content[startint:endint])
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data ={"Email": loginname,
    "Password": Password,
    "RememberMe": ""
    # "__RequestVerificationToken": RequestVerificationToken
    }
    # 登录
    html2 = S.post(url=url, data=data, headers=headers, allow_redirects=True)
    # 页面跳转
    html3 = S.get(url=html2.url, allow_redirects=False)
    cookie = ''
    for name, value in S.cookies.items():
        cookie += '{0}={1};'.format(name, value)
    cookies_dict = requests.utils.dict_from_cookiejar(S.cookies)
    data = {"cookies": cookie, "X-XSRF-TOKEN": cookies_dict["XSRF-TOKEN"]}
    return data


def get_gh_token():
    url = "https://uat-gh-webportal.pg.com.cn/Account/login?RequestPath=%2F"
    response = requests.get(url=url)
    cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
    # print(cookies_dict)
    need_token = "Bearer " + cookies_dict[".AspNetCore.Antiforgery.XAm5jJynw88"]
    return need_token



#-------------UAT-----------------------
# def get_gh_token():
#     url = "https://uat-gh-webportal.pg.com.cn/Account/login?RequestPath=%2F"
#     response = requests.get(url=url)
#     cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
#     # print(cookies_dict)
#     need_token = "Bearer " + cookies_dict[".AspNetCore.Antiforgery.XAm5jJynw88"]
#     return need_token
#
#
# def get_ghweb_token(loginname, Password):
#     S = requests.session()
#     url = "https://uat-gh-webportal.pg.com.cn/Account/login?RequestPath=%2F"
#     response = S.get(url=url)
#     # 获取页面内容：RequestVerificationToken
#     content = str(response.content)
#     # startint = int(content.find('"__RequestVerificationToken" type="hidden" value="')) + 50
#     # endint = startint + 155
#     # RequestVerificationToken = re.findall('"__RequestVerificationToken" type="hidden" value="(.*?)"', content)[0]
#     # print(content[startint:endint])
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     data = {"Email": loginname,
#             "Password": Password,
#             "RememberMe": ""
#             # "__RequestVerificationToken": RequestVerificationToken
#             }
#     # 登录
#     html2 = S.post(url=url, data=data, headers=headers, allow_redirects=True)
#     # 页面跳转
#     html3 = S.get(url=html2.url, allow_redirects=False)
#     cookie = ''
#     for name, value in S.cookies.items():
#         cookie += '{0}={1};'.format(name, value)
#     cookies_dict = requests.utils.dict_from_cookiejar(S.cookies)
#     data = {"cookies": cookie, "X-XSRF-TOKEN": cookies_dict["XSRF-TOKEN"]}
#     return data


#-------------prod-------------------
# def get_skii_token(num=0, token_true=True):
#     S = requests.session()
#     url1 = 'https://fedauth.pg.com.cn/as/authorization.oauth2'
#     params1 = {
#         "scope": "openid profile",
#         "response_type": "code",
#         "pfidpadapterid": "ad..OAuth",
#         "client_id": "PAAS B2B QA SSOFED",
#         "redirect_uri": "https://api-b2b-qa.cn-pgcloud.com/paas-ssofed/v1/auth?app=GhrGAWeb&subscription-key=2787a94d8fe9405fbccde0160a85c591"
#     }
#
#     n = 0
#     html1 = ""
#     while not html1 and n < 3:
#         try:
#             html1 = S.get(url1, params=params1)
#         except ConnectionError:
#             n += 1
#     html1.encoding = 'utf-8'
#     resultlist = re.findall(r'/as/(.*)/resume', html1.text)
#
#     find_text = ','.join(resultlist)
#
#     url2 = 'https://fedauth.pg.com.cn/as/{}/resume/as/authorization.ping'.format(find_text)
#     # print(url2)
#     headers2 = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
#         "Origin": "https://fedauthtst.pg.com.cn",
#         "Referer": "https://fedauthtst.pg.com.cn/",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-Fetch-User": "?1",
#         "Upgrade-Insecure-Requests": "1",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
#     }
#
#     body = {
#         'pf.username': 'ghr.t.7',
#         'pf.pass': 'Gdnchina2',
#         # 'pf.username': 'qin.wh',
#         # 'pf.pass': '123456Aa',
#         'pf.ok': 'clicked',
#         'pf.adapterId': 'OAuth'
#     }
#
#     r = S.post(url2, headers=headers2, data=body, allow_redirects=True)
#
#     try:
#         code = r.url.split('code=')[1].split('&')[0]
#     except Exception as e:
#         if token_true:
#             for i in range(5):
#                 try:
#                     token = get_skii_token(i, token_true=False)
#                     if token:
#                         return token
#                 except:
#                     continue
#             raise Exception('获取token失败')
#
#     url3 = 'https://qa-ga-webportal.pg.com.cn/api/v1/ga/console/gaweb/sso/auth?authCode={}'.format(code)
#     headers3 = {
#         "Accept": "application/json, text/plain, */*",
#         "Referer": "https://qa-ga-webportal.pg.com.cn/login",
#         "Sec-Fetch-Mode": "cors",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
#     }
#     r2 = S.get(url=url3, headers=headers3)
#     # print(r2.json()['accessToken'])
#     return r2.json()['token']
#
#
# print(get_skii_token())
#
#
# def get_gh_token():
#     url = "https://qa-gh-webportal.pg.com.cn/Account/login?RequestPath=%2F"
#     response = requests.get(url=url)
#     cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
#     # print(cookies_dict)
#     need_token = "Bearer " + cookies_dict[".AspNetCore.Antiforgery.KM1ynx8UCww"]
#     return need_token
# # print(get_gh_token)


# def get_gaapp_token(idpUser, idp_cred):
#     S = requests.session()
#     S.keep_alive = False
#     loginurl = "https://auth.cn-pgcloud.com/login"
#     html = S.get(loginurl)
#     # print(html4.content)
#     content = str(html.content)
#     # startint = int(content.find('"X-CSRF-TOKEN" content=')) + 24
#     # endint = startint + 36
#     # CSR = content[startint:endint]
#     CSR = re.findall('"X-CSRF-TOKEN" content="(.*?)"', content)[0]
#     # print(startint)
#     # print(endint)
#     # print(content[startint:endint])
#     url = "https://auth.cn-pgcloud.com/signin"
#     headers = {"Host":"auth.cn-pgcloud.com",
#     "Content-Type"          : "application/x-www-form-urlencoded; charset=UTF-8",
#     "Accept"                :"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Referer"               : "https://auth.cn-pgcloud.com/login",
#     "Origin"                : "https://auth.cn-pgcloud.com"}
#     url2 = "https://auth.cn-pgcloud.com/oauth/authorize?response_type=code&scope=read&client_id=88725d1457f48078d25215dee429bdcauxksxfiu63f&redirect_uri=https%3A%2F%2Fgoldenambassador.pg.com.cn"
#     loginparams = {
#     "_enterprise_id"        : "pg",
#     "_csrf"                 : CSR,
#     "loginRedirectUrl"      : url2,
#     "idpUser"               : idpUser, #13683221270
#     "idp_cred"              : idp_cred #"New201907"
#     }
#     html1                   = S.post(url, headers=headers, data=loginparams, allow_redirects=True)
#     code                    = html1.url.split('code=')[1]
#     # print(code)
#     ghr_url = "https://goldenambassador.pg.com.cn/idp/login?code=" + code
#     html3 = S.get(html1.url, allow_redirects=True)
#     html4 = S.post(ghr_url, allow_redirects=True)
#     # print(html4.content)
#     return 'Bearer' + ' '+ json.loads(html4.content)['token']
