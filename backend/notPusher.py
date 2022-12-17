import hashlib
import random
from time import time
import requests
import base64
from Crypto.Cipher import AES

class NotPusher(object):
    sToken = 'dasdADWdawdaSDadada'
    sEncodingAESKey='6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt'
    key = base64.b64decode(sEncodingAESKey+"=")
    assert len(key) == 32
    
    headers = {
        'User-Agent' :"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }

    def AES_Encrypt(self, data):
        """
        example
            >>> AES_Encrypt('用户zhangjiawei')
            data1: | b'\xe7\x94\xa8\xe6\x88\xb7zhangjiawei' |
            data2: | b'\xe7\x94\xa8\xe6\x88\xb7zhangjiawei\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f' |
            encryptedbytes: | b"\xd3\xa2\xe9\x94w\x95 \xcd{\x11\x18z'\xcd(\x9eZ@\x07\xfb\x07X0#=\xd1\xe4O\x84\xa9\xa6\x8f" |
            encodestrs: | b'06LplHeVIM17ERh6J80onlpAB/sHWDAjPdHkT4Sppo8=' |
            enctext: | 06LplHeVIM17ERh6J80onlpAB/sHWDAjPdHkT4Sppo8= |
        """
        vi = '0102030405060708'
        # utf-8编码 str -> bytestring
        data1 = data.encode('utf8')
        #print('data1: |',data1,'|')
        # bytestring补全到16的倍数
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode('utf-8')
        data2 = pad(data1)
        #print('data2: |',data2,'|')
        # 密钥加密 bytestring -> bytes
        cipher = AES.new(self.key, AES.MODE_CBC, vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data2)
        #print('encryptedbytes: |',encryptedbytes,'|')
        # Base64编码 bytes-> bytestring
        encodestrs = base64.b64encode(encryptedbytes)
        #print('encodestrs: |',encodestrs,'|')
        #  utf-8解码 bytestring -> str
        enctext = encodestrs.decode('utf8')
        #print('enctext: |',enctext,'|')
        return enctext

    def AES_Decrypt(self, data):
        vi = '0102030405060708'
        # utf-8编码  str -> bytestring
        data = data.encode('utf-8')
        # Base64解码 bytestring -> bytes
        encodebytes = base64.b64decode(data)
        # 解密       bytes -> bytestring
        cipher = AES.new(self.key, AES.MODE_CBC, vi.encode('utf-8'))
        text_decrypted = cipher.decrypt(encodebytes)
        # 去掉末尾的补位字符 bytestring
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # utf-8解码 bytestring -> str 
        text_decrypted = text_decrypted.decode('utf-8')
        return text_decrypted
    
    def getSHA1(self, encrypt:str, timestamp:str, nonce:str):
        """用SHA1算法生成安全签名
        @param encrypt: 密文
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 安全签名
        """
        try:
            sortlist = [self.sToken, timestamp, nonce, encrypt]
            sortlist.sort()
            sha = hashlib.sha1()
            sha.update("".join(sortlist).encode('utf-8'))
            return  sha.hexdigest()
        except Exception as e:
            print(e)
            return  None
        
    def send_text(self, fromUser:str, toUser:str, text:str):
        # 加密数据
        encryptMsg = self.AES_Encrypt(text)
        # 生成签名
        timestamp = str(int(time()))
        nonce = ''.join([str(random.randint(0,9)) for _ in range(10)])
        signature = self.getSHA1(encryptMsg, timestamp, nonce)
        
        url = 'http://1.117.65.89:33/send'
        
        data = {
            'fromUser':   fromUser,
            'toUser' :    toUser,
            'encryptMsg': encryptMsg,
            'signature' : signature,
            'timestamp' : timestamp,
            'nonce' : nonce,
        }
        
        resp = requests.post(url=url, headers=self.headers, json=data)
        print(resp,resp.text)

pusher = NotPusher()
# 推送消息测试
# x = pusher.send_text('auto_clock','zhangjiawei','哈哈哈')

