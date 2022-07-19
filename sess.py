import random
import requests
from colors import bcolors

# Proxy Types:
#       1-HTTP 2-Socks4 3-Socks5 4-ProxyLess | http , socks4 , socks5 , proxyless



def GetProxyAuth(proxy_type):

    lines = open('proxy.txt').read().splitlines()
    proxies_file = random.choice(lines)
    proxies = {}
    a = random.choice(proxies_file)
    b = str(a).split(':')
    c = b[2] + ':' + b[3] + '@' + b[0] + ':' + b[1]

    if proxy_type == 1:
        proxies = {
            "http": "http://{0}".format(c),
            "https": "http://{0}".format(c)
        }
    elif proxy_type == 2:
        proxies = {
            "https": "http://{0}".format(c)
        }
    elif proxy_type == 3:
        proxies = {
            "http": "socks4://{0}".format(c)
        }
    else:

        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies




def GetProxyNormal(proxy_type):
    lines = open('proxy.txt').read().splitlines()
    proxies_file = random.choice(lines)
    if proxy_type == 1:
        proxies = {
            "http": f'http://{proxies_file}',
            "https": f'http://{proxies_file}'
        }
    elif proxy_type == 2:
        proxies = {
            "http": f'socks4://{proxies_file}',
            "https": f'socks4://{proxies_file}'
        }
    elif proxy_type == 3:
        proxies = {
            "http": f'socks5://{proxies_file}',
            "https": f'socks5://{proxies_file}'
        }

    else:

        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies


def detectAndReturnProxy(proxy_type):


    lines = open('proxy.txt').read().splitlines()
    proxy = random.choice(lines).strip()
    dig = proxy.split(':')
    len = dig.__len__()

    if len == 2:
        proxies = GetProxyNormal(proxy_type)
    elif len ==4:
        proxies = GetProxyAuth(proxy_type)

    else:
        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies



def sess(headers):
    s = requests.session()

    if headers != None and headers != '':
        s.headers = headers

    return s


def sessProxy(headers , proxy_type):
    s = requests.session()

    if headers != None:
        s.headers = headers

    s.proxies = detectAndReturnProxy(proxy_type)

    return s
