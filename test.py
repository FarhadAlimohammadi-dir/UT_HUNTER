import requests

from engine import engine

eng = engine(True)
eng.crawl('http://192.168.134.129/',4,True,4)
#
# #eng.setInfo()
#eng.startXSS_get_param(True,4)


#eng.startSQL_get_form(4)
eng.startLFI(4)


