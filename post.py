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
    "kakaoId": "1111",
    "username": "이준하",
}
# 딕셔너리를 JSON으로 변환 
data = json.dumps(temp)


response = requests.post(url, headers=headers, data=data)

print("response: ", response)
print(type(response))
print(response.json())
#result=eval(response.text)
#print(result.get('result'))

#print(D['result'])