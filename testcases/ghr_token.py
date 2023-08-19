import requests

import re

import json

import jsonpath as jsonpath

from bs4 import BeautifulSoup



# 1.获取GA APP的token（ISA）
def test_get_gaapp_isa_token(idpUser, idp_cred):
    S = requests.session()
    S.keep_alive = False
    loginurl = "https://authtst.cn-pgcloud.com/login"
    html = S.get(loginurl,verify=False)
    # res = html.text
    # print(res)
    content = str(html.text)
    # print(content)
    CSR = re.search('"X-CSRF-TOKEN" content="(.*?)"', content).group(1)
    # CSR = re.findall('"X-CSRF-TOKEN" content="(.*?)"', content)[0]
    # print(CSR)
    # print(endint)
    # print(content[startint:endint])
    url = "https://authtst.cn-pgcloud.com/signin"
    headers = {"Host": "authtst.cn-pgcloud.com",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Referer": "https://authtst.cn-pgcloud.com/login",
               "Origin": "https://authtst.cn-pgcloud.com",
               "Cache-Control": "max-age=0",
               "X-Requested-With": "com.pactera.pgsit"}
    url2 = "https://authtst.cn-pgcloud.com/oauth/authorize?response_type=code&scope=read&client_id=73d372abafb6936e85b941998cf03bed5AcRf8N8bY8&redirect_uri=https%3A%2F%2Fga-bff.pg.com.cn&state=a3slozfn"
    loginparams = {
        "_enterprise_id": "pg",
        "_csrf": CSR,
        "loginRedirectUrl": url2,
        "idpUser": idpUser,  # ISA登录的手机号码：13683221270
        "idp_cred": idp_cred  # ISA的账号密码："New201907"
    }
    # print(loginparams)
    html1 = S.post(url, headers=headers, data=loginparams, allow_redirects=True,timeout=5)
    code = html1.url.split('code=')[1]
    # print(code)
    ghr_url = "https://qa-ga-bff.pg.com.cn/api/v1/ga/app/idp/login?code=" + code
    headers = {
        "Host":"qa-ga-bff.pg.com.cn",
        "Content-Type":"application/json; charset=utf-8",
        "accept":"application/json, text/plain, */*",
        "appversion":"3.1.0",
        "mobilephone":"Android 9",
        "uniqueid":"2e6d5248b19b4905",
        "User-Agent":"okhttp/3.12.1",
        "Connection":"keep-alive"
    }
    json = {}
    # html3 = S.get(html1.url, allow_redirects=True)
    html4 = S.post(ghr_url, headers=headers,json=json,allow_redirects=True,verify=False,timeout=5)
    # print(html4.json())
    # result = html4.json()
    # token_name = jsonpath.jsonpath(result,'$..token')
    # print("".join(token_name))
    # return 'Bearer' +' '+"".join(token_name)
    return 'Bearer {}'.format(html4.json()['token'])


# print(test_get_gaapp_isa_token("15890072779","New201907"))


# 2.获取gaweb的token
def test_get_gaweb_token(idpUser,idp_cred):
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
    # return 'Bearer {}'.format(json.loads(html3.content)['token'])
    token = 'Bearer {}'.format(json.loads(html3.content)['token'])
    return token


# print(test_get_gaweb_token('wei.ws.7', 'Ht1pailRinfox#gKs9M:2'))


# 获取GH APP的登录token
def test_gh_app_token():
    """
    :param User_ID:SO账户（1043），加密后传参
    :param User_Password: SO账户密码（aaabbb），加密后传参
    :return:request.Response.LoginInfo.User_openId 用户签名
    """
    S = requests.session()
    S.keep_alive = False
    url = "https://qa-gh-bff.pg.com.cn//api/Base/Login"
    headers = {
        "Ocp-Apim-Subscription-Key":"9bc6b2db6bd948e5837a3f557aadcf18",
        "Content-Type":"application/json; charset=utf-8",
        "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 10; SCM-W09 Build/HUAWEISCM-W09)",
        "Host":"qa-gh-bff.pg.com.cn",
        "Connection":"Keep-Alive"
    }
    data = {
        "Device_Type": "HUAWEI SCM-W09",
        "User_Password": "gAhBtNGGLds\/BnsB\/9dQa5l6nMORekXmjsHjK0Eyn5xFx1t5pASaRBlM4Q2wdo+LuUC7wpzLTJsJ\nua690pm2p0Og7lK7N1BNu6FRIlfDwuoEl50BwFL0Z6SrWLVTDVvqGhGCWR59aVRm\/T4GV2ONDdPT\nb9pTbtkYFsyZwFNaQo4=\n",
        "IP_Address": "192.168.1.104",
        "User_OpenId": "",
        "Lock_Status": "0",
        "Device_System": "SCM-W09,29,10",
        "User_ID": "zWpiXaTXJox6ugBGEyTX4RpVtgi9IP1KZOqbEfEbTL8ilcv\/XAiU40jXnhdqn8Z2FnZFvzgrQlgC\n7hPoROJB\/wtTQ+BUaVX1E6yGhnR22FnDHfYzILaRnkfWvfoaQAXtnc8wDEJOv3uI1xC6a7ZX\/jOi\nDUoOXdOGbYvGkxHJpBc=\n",
        "App_Type": "1"
    }
    html = S.post(url=url,headers=headers,json=data,allow_redirects=True,verify=False,timeout=5)
    # print(html.text)
    result = html.json()
    User_openId = jsonpath.jsonpath(result,'$.LoginInfo.User_OpenId')
    # print("".join(User_openId))
    return "".join(User_openId)

# print(test_gh_app_token())

# 获取GH APP的登录token
def test_gh_app_token2():
    """
    :param User_ID:SO账户（1043），加密后传参
    :param User_Password: SO账户密码（aaabbb），加密后传参
    :return:request.Response.LoginInfo.User_openId 用户签名
    """
    S = requests.session()
    S.keep_alive = False
    url = "https://qa-gh-bff.pg.com.cn//api/Base/Login"
    headers = {
        "Ocp-Apim-Subscription-Key":"9bc6b2db6bd948e5837a3f557aadcf18",
        "Content-Type":"application/json; charset=utf-8",
        "User-Agent":"Dalvik/2.1.0 (Linux; U; Android 10; SCM-W09 Build/HUAWEISCM-W09)",
        "Host":"qa-gh-bff.pg.com.cn",
        "Connection":"Keep-Alive"
    }
    data = {
        "Device_Type": "HUAWEI SCM-W09",
        "User_Password": "gAhBtNGGLds\/BnsB\/9dQa5l6nMORekXmjsHjK0Eyn5xFx1t5pASaRBlM4Q2wdo+LuUC7wpzLTJsJ\nua690pm2p0Og7lK7N1BNu6FRIlfDwuoEl50BwFL0Z6SrWLVTDVvqGhGCWR59aVRm\/T4GV2ONDdPT\nb9pTbtkYFsyZwFNaQo4=\n",
        "IP_Address": "192.168.1.104",
        "User_OpenId": "",
        "Lock_Status": "0",
        "Device_System": "SCM-W09,29,10",
        "User_ID": "zWpiXaTXJox6ugBGEyTX4RpVtgi9IP1KZOqbEfEbTL8ilcv\/XAiU40jXnhdqn8Z2FnZFvzgrQlgC\n7hPoROJB\/wtTQ+BUaVX1E6yGhnR22FnDHfYzILaRnkfWvfoaQAXtnc8wDEJOv3uI1xC6a7ZX\/jOi\nDUoOXdOGbYvGkxHJpBc=\n",
        "App_Type": "1"
    }
    html = S.post(url=url,headers=headers,json=data,allow_redirects=True,verify=False,timeout=5)
    # print(html.text)
    result = json.loads(html.text)
    # print(result)
    return result['LoginInfo']['User_OpenId']
    # User_openId = jsonpath.jsonpath(result,'$.LoginInfo.User_OpenId')
    # print("".join(User_openId))
    # return "".join(User_openId)

print(test_gh_app_token2())

# 获取Mini isp的token
def test_get_gaapp_isp_token(idpUser, idp_cred):
    S = requests.session()
    S.keep_alive = False
    isp_url = 'https://qa-internal-api-b2b.cn-pgcloud.com/api/ghr-attendance-service-ghrprd/api/v1/isp/schedule/add' # 推送ISP排班
    json = {
        "allocationListId": "SL202303271731925931",
        "category": "",
        "executionRange": "20230729 00:00:00-20230820 00:00:00",
        "isOnDuty": "1",
        "planTime": "9:15-20:30,12:00-13:00",
        "promoterId": "1000276889",
        "promoterPhone": "15890072779",
        "starLevel": "",
        "storeCode": "80065828",
        "ispType": "",
        "agencyCode": "MC",
        "agency": "Mecool:明酷",
        "planInteractionPsd": "0"
    }
    isp_url1 = S.post(url=isp_url, json=json,verify=False,timeout=20)
    # print(isp_url1.content)
    loginurl = "https://authtst.cn-pgcloud.com/login"
    html = S.get(loginurl)
    # res = html.text
    # print(res)
    content = str(html.text)
    # print(content)
    CSR = re.search('"X-CSRF-TOKEN" content="(.*?)"', content).group(1)
    # CSR = re.findall('"X-CSRF-TOKEN" content="(.*?)"', content)[0]
    # print(CSR)
    # print(endint)
    # print(content[startint:endint])
    url = "https://authtst.cn-pgcloud.com/signin"
    headers = {"Host": "authtst.cn-pgcloud.com",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Referer": "https://authtst.cn-pgcloud.com/login",
               "Origin": "https://authtst.cn-pgcloud.com",
               "Cache-Control": "max-age=0",
               "X-Requested-With": "com.pactera.pgsit"}
    url2 = "https://authtst.cn-pgcloud.com/oauth/authorize?response_type=code&scope=read&client_id=73d372abafb6936e85b941998cf03bed5AcRf8N8bY8&redirect_uri=https%3A%2F%2Fga-bff.pg.com.cn&state=a3slozfn"
    loginparams = {
        "_enterprise_id": "pg",
        "_csrf": CSR,
        "loginRedirectUrl": url2,
        "idpUser": idpUser,  # ISA登录的手机号码：13683221270
        "idp_cred": idp_cred  # ISA的账号密码："New201907"
    }
    html1 = S.post(url, headers=headers, data=loginparams, allow_redirects=True, timeout=5)
    code = html1.url.split('code=')[1]
    ghr_url = "https://qa-ga-bff.pg.com.cn/api/v1/ga/app/idp/login?code=" + code
    headers = {
        "Host":"qa-ga-bff.pg.com.cn",
        "Content-Type":"application/json; charset=utf-8",
        "accept":"application/json, text/plain, */*",
        "appversion":"3.1.0",
        "mobilephone":"Android 9",
        "uniqueid":"2e6d5248b19b4905",
        "User-Agent":"okhttp/3.12.1"
    }
    json = {}
    html4 = S.post(ghr_url, headers=headers,json=json,verify=False,allow_redirects=True,timeout=5)
    # result = html4.json()
    # print(type(result))
    token = html4.json()["token"]
    print(token)
    return 'Bearer' +' '+ token
    # token_name = jsonpath.jsonpath(result,'$..token')
    # print("".join(token_name))
    # return 'Bearer' +' '+"".join(token_name)


# print(test_get_gaapp_isp_token("15890072779","New201907"))


def add_atendance():
    """
    服务商推送排班
    :return:
    """
    S = requests.session()
    S.keep_alive = False
    url = "https://qa-internal-api-b2b.cn-pgcloud.com/api/ghr-attendance-service-ghrprd/api/v1/isp/schedule/add"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    json = {
        "allocationListId": "SL202303271731925931",
        "category": "",
        "executionRange": "20230729 00:00:00-20230820 00:00:00",
        "isOnDuty": "1",
        "planTime": "9:15-20:30,12:00-13:00",
        "promoterId": "1000276889",
        "promoterPhone": "15890072779",
        "starLevel": "",
        "storeCode": "80065828",
        "ispType": "",
        "agencyCode": "MC",
        "agency": "Mecool:明酷",
        "planInteractionPsd": "0"
    }
    html = S.post(url=url, headers=headers,json=json, verify=False, timeout=5)
    print(html.json())
# print(add_atendance)