from urllib.parse import urljoin

from sess import *
from bs4 import BeautifulSoup
from engine import *

class crawler:


    visited = []



    @classmethod

    def startCrawl(self,targetUrl,proxy_type,headers,depth):
        urlList = self.getFirstPageLinks(targetUrl,proxy_type,headers)
        self.crawUrls(urlList,proxy_type,headers,depth)

    @classmethod
    def getFirstPageLinks(self,targetUrl,proxy_type,headers):


        urlList = []

        if proxy_type == 4 or 'proxyless' in proxy_type:
            session = sess(headers)

        else:
            session = sessProxy(headers,proxy_type)

        firstPage = session.get(targetUrl).text
        #print(firstPage)

        isi = BeautifulSoup(firstPage, "html.parser")

        for obj in isi.find_all("a", href=True):
            url = obj["href"]
            #print(urljoin(targetUrl, url))

            if urljoin(targetUrl, url) in self.visited:
                continue

            elif url.startswith("mailto:") or url.startswith("javascript:") or '#' in url :
                continue

            elif url.startswith(targetUrl) or "://" not in url:
                urlList.append(urljoin(targetUrl, url))
                self.visited.append(urljoin(targetUrl, url))

        return urlList


    @classmethod

    def crawUrls(self,urlsList,proxy_type,headers,depth):
        for url in urlsList:
            newLinks = self.getFirstPageLinks(url,proxy_type,headers)
            depth -= 1
            if not depth <= 0:
                    self.crawUrls(newLinks,proxy_type,headers,depth)


