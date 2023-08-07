# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 01:42:00 2023

@author: juLeena
"""

import requests
import json

url = "http://3.39.118.25:5000/journal"

# headers
headers = {
    "Content-Type": "application/json"
}

# data
temp = {
    "userDto": {
        "kakaoId": "101010",
        "username": "박유리",
        "age": 22,
        "gender": "여자",
        "job": "대학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "00:00:00",
            "dateTime": "2023-06-16T00:00:00",
            "stamp": "졸림",
            "memoLet": "과제... 할 건 많은데 막상 과제 하러 들어가면 뭐부터 손대야 할지 감이 안 온다. 그래도 제일 어려운 부분 오늘 끝내서 내일이면 얼추 완성시킬 수 있을 것 같다"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "01:03:00",
            "dateTime": "2023-06-16T01:03:00",
            "stamp": "졸림",
            "memoLet": "점심으로 친구들이랑 초밥 먹었다 맛은 그냥 무난! 지금 밥 다 먹고 친구들이랑 대외활동 자료 작성 잠깐 하다가 헤어져서 학사 가는 길인데... 너무 피곤하다"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "23:59:00",
            "dateTime": "2023-06-16T23:59:00",
            "stamp": "졸림",
            "memoLet": "넘졸려서 조금만 자고 과제해야할듯... 진짜피곤하다아악"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "23:59:00",
            "dateTime": "2023-06-16T23:59:00",
            "stamp": "졸림",
            "memoLet": "저녁먹고 산책나왔다! 기분 좋음"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-16",
            "localTime": "23:59:00",
            "dateTime": "2023-06-16T23:59:00",
            "stamp": "졸림",
            "memoLet": "저녁 먹고 잔깐 산책나왔는데 메가커피 앞에서 사감쌤 마주쳤다! 사감쌤이 먹고싶은 거 사주신다고 얼른 고르래서 박웬수랑 나랑 마카롱 하나 슈크림빵 하나 골랐음... 아껴뒀다 나중에 먹어야지"
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