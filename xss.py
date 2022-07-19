import requests
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse,parse_qs,urlencode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import engine
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sess
from engine import *
from sess import *
from log import *
import urllib.parse as urlparse



class xss:

    def __init__(self):
        self.proxy_type = 0
        self.headers = ''
        self.payload = '<script> alert(1) </script>'


    def setInfo(self,headers,proxy_type):
        self.proxy_type = proxy_type
        self.headers = headers



    def xss_get_form(self,url):

        sess = self.sess()
        txt = sess.get(url).text

        bsObj = BeautifulSoup(txt, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "get":

                Log.warning("Url using GET method XSS: "  + urljoin(url, action))
                Log.info("Getting inputs ...")

                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            keys.update({key["name"]: key["name"]})

                        else:
                            keys.update({key["name"]: self.payload})

                    except Exception as e:
                        Log.info("Internal error: " + str(e))
                        try:
                            keys.update({key["name"]: self.payload})
                        except KeyError as e:
                            Log.info("Internal error: " + str(e))

                Log.info("Sending payload (GET) method...")

                req = sess.get(urljoin(url, action), params=keys)
                if self.payload in req.text:
                    Log.high("Detected XSS (GET) at " + url)
                    file = open("xss_get.txt", "a+")
                    file.write(str(urljoin(url, action)) + "\n\n")
                    file.close()
                    Log.high("GET data: " + str(keys))
                else:
                    Log.info("Page using GET_FORM method but XSS vulnerability not found")



    def xss_get_param(self,url: str):

        sess = self.sess()

        if '&' not in url:
            return

        parsed = urlparse.urlparse(url)
        querys = parsed.query.split("&")

        new_query = "&".join(["{}{}".format(query.replace(query.split('=')[1], ''), self.payload) for query in querys])
        parsed = parsed._replace(query=new_query)
        url = urlparse.urlunparse(parsed)

        Log.warning("Found link GET Method: " + url)

        if not url.startswith("mailto:") and not url.startswith("tel:"):
            req = sess.get(url, verify=False)
            if self.payload in req.text:
                Log.high("Detected XSS (GET) at " + req.url)
                file = open("xss_get_params.txt", "a+")
                file.write(str(req.url) + "\n")
                file.close()

            else:
                Log.info("Page using GET method but XSS vulnerability not found")
        else:
            pass



    def xss_post(self,url):

        sess = self.sess()

        txt = sess.get(url).text

        bsObj = BeautifulSoup(txt, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "post":

                Log.warning("Url using POST method XSS: " + url)
                Log.info("getting fields ...")

                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            Log.info("Form key name: " +  key["name"] + " value: " +  "<Submit Confirm>")
                            keys.update({key["name"]: key["name"]})

                        else:
                            Log.info("Form key name: " +  key["name"] + " value: " +  self.payload)
                            keys.update({key["name"]: self.payload})

                    except Exception as e:
                        Log.info("Internal error: " + str(e))


                Log.info("Sending XSS payload (POST) method ..")
                req = sess.post(urljoin(url, action), data=keys)
                if self.payload in req.text:
                    Log.high("Detected XSS (POST) at " + urljoin(url, action))
                    file = open("xss_post.txt", "a+")
                    file.write(str(urljoin(url, action)) + "\n" + str(keys) + '\n\n')
                    file.close()
                    Log.high("Post data: " + str(keys))
                else:
                    Log.info("Page using POST method but XSS vulnerability not found")


    def sess(self):

        if self.proxy_type == 4:
            session = sess(self.headers)

        else:
            session = sessProxy(self.headers,self.proxy_type)

        return session