import json
import time

import requests

data = {"suid":123477777,"sid":None,"stime":"2022-05-01 09:48:40","sname":"哑铃","scount":50,"sscore":98}
url = "http://localhost:8085/addsportdata"
r = requests.post(url, data)






