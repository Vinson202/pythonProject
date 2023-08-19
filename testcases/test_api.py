import re

from commons.request_util import RequestUtil
from commons.yaml_util import write_yaml, read_yaml

import urllib3

from testcases.ghr_test import json


class TestTokenApi:


    def test_get_gaapp_isa_token(self,idpUser="15890072779",idp_cred="New201907"):
        """
        获取ISA的token
        :param idpUser: 15890072779
        :param idp_cred: New201907
        :return:
        """
        RequestUtil.all_send_request.keep_alive = False
        loginurl = "https://authtst.cn-pgcloud.com/login"
        urllib3.disable_warnings()
        html = RequestUtil().all_send_request(method="get", url=loginurl, verify=False)
        content = str(html.text)
        # 提取csr并写入extract.yaml文件
        CSR = re.search('"X-CSRF-TOKEN" content="(.*?)"', content).group(1)
        datas = {"isa_csrf":CSR}
        write_yaml(datas)
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
            "_csrf": read_yaml("isa_csrf"),
            "loginRedirectUrl": url2,
            "idpUser": idpUser,  # ISA登录的手机号码
            "idp_cred": idp_cred  # ISA的账号密码："New201907"
        }
        html1 = RequestUtil().all_send_request(method="POST", url=url, headers=headers, data=loginparams,
                                             allow_redirects=True, timeout=5)
        code = html1.url.split('code=')[1]
        data_code = {"isa_data_code":code}
        write_yaml(data_code)
        # print(code)
        ghr_url = "https://qa-ga-bff.pg.com.cn/api/v1/ga/app/idp/login?code=" + read_yaml("isa_data_code")
        headers = {
            "Host": "qa-ga-bff.pg.com.cn",
            "Content-Type": "application/json; charset=utf-8",
            "accept": "application/json, text/plain, */*",
            "appversion": "3.1.0",
            "mobilephone": "Android 9",
            "uniqueid": "2e6d5248b19b4905",
            "User-Agent": "okhttp/3.12.1",
            "Connection": "keep-alive"
        }
        json = {}
        # html3 = S.get(html1.url, allow_redirects=True)
        urllib3.disable_warnings()
        html4 = RequestUtil().all_send_request(method="POST", url=ghr_url, headers=headers, json=json,
                                             allow_redirects=True, verify=False, timeout=5)
        data_token = {"isa_token":'Bearer {}'.format(html4.json()['token'])}
        write_yaml(data_token)
        # return 'Bearer {}'.format(html4.json()['token'])


    def test_gh_app_token(self):
        """
        获取SO的登录签名
        :param User_ID: SO账户（1043），加密后传参
        :param User_Password: SO账户密码（aaabbb），加密后传参
        :return:request.Response.LoginInfo.User_openId 用户签名
        """
        RequestUtil.all_send_request.keep_alive = False
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
        html = RequestUtil.all_send_request(method="POST",url=url,headers=headers,json=data,allow_redirects=True,verify=False,timeout=5)
        # print(html.text)
        result = json.loads(html.text)
        token_data = {"SO_Token": result['LoginInfo']['User_OpenId']}
        write_yaml(token_data)
        # print(result)
        # return result['LoginInfo']['User_OpenId']
        # User_openId = jsonpath.jsonpath(result,'$.LoginInfo.User_OpenId')
        # print("".join(User_openId))
        # return "".join(User_openId)