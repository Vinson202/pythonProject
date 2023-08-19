import json
import re

import requests
from bs4 import BeautifulSoup


class TestApi:

    # 1、获取refresh_token
    def do_refresh_token(subscription_key, refresh_token, base_url):
        """使用refresh_token 刷新并返回access_token

        :param subscription_key:   订阅ID  2787a94d8fe9405fbccde0160a85c591
        :param refresh_token: refresh_token
        :param base_url: 鉴权地址  例：https://api-b2b-qa.cn-pgcloud.com/paas-ssofed
        :return: access_token
        """
        url = base_url + "/v3/token/refresh"
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": subscription_key}
        json_data = {"refresh_token": refresh_token}
        try:
            res = requests.post(url, headers=headers, json=json_data, allow_redirects=False, verify=False, timeout=30)
        except Exception as e:
            raise Exception("请求刷新接口失败, 具体原因：{}".format(str(e.args)))

        if res.status_code == 200:
            try:
                access_token = res.json()["access_token"]
            except Exception as e:
                raise Exception("接口响应中没有access_token, 具体响应：" + str({
                    "status_code": res.status_code, "text": res.text, "json": res.json()}))
            else:
                return access_token
        else:
            raise Exception("不是成功的接口响应, 具体响应：" + str({
                "status_code": res.status_code, "text": res.text, "json": res.json()}))


    # print(do_refresh_token('2787a94d8fe9405fbccde0160a85c591','T1NmviNeL9H6fpjJvp1pzbfLaA43','https://api-b2b-qa.cn-pgcloud.com/paas-ssofed/'))

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
        print("html2: ", html2.url)
        code = html2.url.split('code=')[1]
        print("code: ", code)
        url2 = "https://qa-ga-webportal.pg.com.cn/api/v1/ga/console/gaweb/sso/auth?authCode=" + code

        headers2 = {"Referer": "https://qa-ga-webportal.pg.com.cn/login",
                    "Host": "qa-ga-webportal.pg.com.cn",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
                    }
        html3 = S.get(url2, headers=headers2)
        return 'Bearer {}'.format(json.loads(html3.content)['token'])


class TestApi2:

    # 3、获取gaweb的token
    def test_get_gaweb_token(self,idpUser, idp_cred):
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
        token = 'Bearer {}'.format(json.loads(html3.content)['token'])
        print(token)
        return token
        # return 'Bearer {}'.format(json.loads(html3.content)['token'])


    # print(test_get_gaweb_token('wei.ws.7','Ht1pailRinfox#gKs9M:2'))


if __name__ == '__main__':
    TestApi2().test_get_gaweb_token('wei.ws.7','Ht1pailRinfox#gKs9M:2')



