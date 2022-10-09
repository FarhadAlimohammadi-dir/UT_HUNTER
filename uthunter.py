import argparse

import colorama

from engine import engine
from log import Log
colorama.init(wrap=True)

parser = argparse.ArgumentParser(description="UT Hunter Advanced Vulnerability Scanner")
parser.add_argument('-url', type=str, required=True)
parser.add_argument('-proxy', type=str, choices=['http', 'socks4', 'socks5'] , default= 'proxyless' , required=False)
parser.add_argument('-leecher_depth', type=int ,default="0",required=False)
parser.add_argument('-use_header', type=str, choices=['yes',], default="no",required=False)
parser.add_argument('-bug_type', type=str, choices=['lfi','xss','sql'],required=True)
parser.usage = """

Parameters = -url , -proxy , -leecher_depth , -use_header , -bug_type

[1] -url => required
[2] -proxy => default is proxyless | if need use proxy, put proxies in proxies.txt and pass one of http socks4 socks5
[3] -leecher_depth => default is 0 | if needed to use leecher, pass an integer to set depth for leeching from your url
[4] -use_header => default is no | if needed to use header, put headers as netscape format (google chrome inspector headers)
 in headers.txt and pass yes
[5]-bug_type => required and choices are [lfi,xss,sql]
 
"""
opt = parser.parse_args()

if opt.use_header == 'no':
    use_header = False
else:
    use_header = True

if 'http' in str(opt.proxy).lower():
    proxyType = 1
elif 'socks4' in str(opt.proxy).lower():
    proxyType = 2
elif 'socks5' in str(opt.proxy).lower():
    proxyType = 3
else:
    proxyType = 4


if opt.leecher_depth != 0:
    eng = engine(use_header)
    eng.crawl(opt.url, proxyType, use_header, opt.leecher_depth)

else:
    pass

if 'xss' in opt.bug_type:
    Log.info('Starting XSS Get Form ......')
    eng = engine(use_header)
    eng.startXSS_get_form(proxyType)
    Log.info('XSS Get Form Finished.')

    Log.info('Starting XSS POST ......')
    eng.startXSS_post(proxyType)
    Log.info('XSS POST Finished.')

    Log.info('Starting XSS Param ......')
    eng.startXSS_get_param(proxyType)
    Log.info('XSS Param Finished.')

elif 'sql' in opt.bug_type:

    Log.info('Starting SQL Get Form ......')
    eng = engine(use_header)
    eng.startSQL_get_form(proxyType)
    Log.info('SQL Get Form Finished.')

    Log.info('Starting SQL Param ......')
    eng.startSQL_get_param(proxyType)
    Log.info('SQL Param Finished.')

    Log.info('Starting SQL Post ......')
    eng.startSQL_post(proxyType)
    Log.info('SQL Post Finished.')


else:
    Log.info('Starting LFI ......')
    eng = engine(use_header)
    eng.startLFI(proxyType)
    Log.info('LFI Finished.')


