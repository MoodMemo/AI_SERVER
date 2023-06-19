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
    "userDto": {
        "kakaoId": "101010",
        "username": "이하은",
        "age": 23,
        "gender": False,
        "job": "학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "00:00:00",
            "dateTime": "2023-06-16T00:00:00",
            "stamp": "졸림",
            "memoLet": "공부 언제 해 큰일남"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "01:03:00",
            "dateTime": "2023-06-16T01:03:00",
            "stamp": "졸림",
            "memoLet": "공부 언제 해 큰일남"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "23:59:00",
            "dateTime": "2023-06-16T23:59:00",
            "stamp": "졸림",
            "memoLet": "공부 언제 해 큰일남"
        }
    ]
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