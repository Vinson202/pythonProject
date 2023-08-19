import requests


class RequestUtil:

    sess = requests.session()

    def all_send_request(self,**kwargs):
        """
        统一请求封装
        :param kwargs:
        :return:
        """
        res = RequestUtil.sess.request(**kwargs)

        return res
