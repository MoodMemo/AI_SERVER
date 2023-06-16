# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 01:42:00 2023

@author: juLeena
"""

import requests
import json

url = "http://127.0.0.1:5000/test"

# headers
headers = {
    "Content-Type": "application/json"
}

# data
temp = {
    "name": "무드메모",
}
# 딕셔너리를 JSON으로 변환 
data = json.dumps(temp)


response = requests.post(url, headers=headers, data=data)

print("response: ", response)
print(type(response))
print(eval(response.text))

#print(D['result'])