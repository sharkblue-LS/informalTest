import base64
from Crypto.Cipher import AES


class EncryptDate:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key.encode("utf8"), AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


# eg = EncryptDate("szewecszewecszew")  # 这里密钥的长度必须是16的倍数
# encrypt_text = eg.encrypt('{"username":"19812341111","password":"a123456","captcha":"1234","captchaId":"01bfe55aa2de42a8b2b163b81a60e3f8","accountType":"PERSONAL","captchaType":"PERSON_LOGIN"}')
# print('encrypt_text : ', encrypt_text)
# decrypt_text = eg.decrypt(encrypt_text)
# print('encrypt_text ：', decrypt_text)

# encrypt_text = eg.encrypt("19812341111")
# print('encrypt_text : ', encrypt_text)
# a='2wStCMf63/eOJ9g7ZaQMUtCquubC6oD0iDsyiBviVicJOhivd27XLWsxMTOlpPu5xJrycfs8xMCIvJCNaXIukA732+nNwkO8qACqbGtDQoYi99DIb8hjPXlHscGczQuu/oh4iANTB+5Owv0tHCsJcTPdOOJ3jmt6kfsVazABWF34WxJM35xVPcXGT9J/TCQyBcbsemnZE3Ix81wC9+RcHsEq+q5lMtkURTAYCSxU20Y='
# decrypt_text = eg.decrypt(a)
# print('a ：', decrypt_text)

import requests
import time
import json

url = 'http://dd-test.gcnao.cn/gateway/account/captcha/image'
params = {'md':int(round(time.time())),'captchaType':'PERSON_LOGIN'}
imageResp = json.loads(requests.get(url,params=params).content)
print(imageResp['result']['id'])
captchaId = imageResp['result']['id']

data = {"username":"19812341111","password":"a123456","captcha":"1234","captchaId":captchaId,"accountType":"PERSONAL","captchaType":"PERSON_LOGIN"}
url1 = 'http://dd-test.gcnao.cn/gateway/account/loginV2'
eg = EncryptDate("szewecszewecszew")
encrypt_text = eg.encrypt(str(data))
print(encrypt_text)
loginResp = requests.post(url1,data={'data':encrypt_text}).content
print(loginResp.decode('utf-8'))
print(json.loads(loginResp)['result'])