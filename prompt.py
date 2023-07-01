# -*- coding: utf-8 -*-

import openai
import os
#import datetime
import time
import tiktoken
#import json
#import requests




def generate_journal(prompt):
    #d = datetime.datetime.now() - datetime.timedelta(days=1) #어제 날짜로 일기 작성
    #date=f'{str(d.year%100):0>2}.{str(d.month):0>2}.{str(d.day):0>2}'
    #week=['월','화','수','목','금','토','일']
    #weekday=week[d.weekday()]
    #tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    #print(text)
    
    start=time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content":f"{prompt}"}],
        temperature=0.1
        )
    end=time.time()
    #print(end-start,'sec')
    """
    print(response.usage)
    output=response.choices[0].message.content
    print(output)
    """
    
    return response.choices[0].message.content, end-start

def make_prompt(age,gender,job,memolet_list):
    let=''
    for i in range(len(memolet_list)):
        date=memolet_list[i].get('dateTime')
        let+=f"{i+1}. {date[:10]} {date[11:16]} {memolet_list[i].get('memoLet')}\n"
    text=f"너는 {age}세 {gender} {job}의 입장에서 주어진 조건에 따라 일기를 작성해주는 assistant야.\n아래 \'\'\'로 구분된 내용을 합쳐 하나의 일기를 써줘.\n이때 일기에는 [제목], [내용], [키워드]가 포함되도록 해줘.\n키워드는 반드시 3개로 뽑아줘.\n1.,2.,3.과 같이 구분된 각 내용들은 오늘 하루 있었던 일들이야.\n일기에 구체적인 시간은 절대 포함하지 마.\n그리고 시간의 흐름만 반영해 일기를 과거형으로 써줘.\n일기 내용은 아래 \'\'\'로 구분된 내용을 기반으로, 과도한 추측은 하지 마.\n제목은 오늘 하루 있었던 일의 핵심을 요약해줘.\n\n\'\'\'\n{let}\'\'\'"
    
    return text

def generate_keyword():
    text=f"아래 \'\'\'로 구분된 각 문단을 대표할 수 있는 키워드를 1~3개 정도 콤마(,)로 구분해서 뽑아줘.\n\n\
    \'\'\'\n\
    1. 과제... 할 건 많은데 막상 과제 하러 들어가면 뭐부터 손대야 할지 감이 안 온다. 그래도 제일 어려운 부분 오늘 끝내서 내일이면 얼추 완성시킬 수 있을 것 같다\n\
    2. 점심으로 친구들이랑 초밥 먹었다 맛은 그냥 무난! 지금 밥 다 먹고 친구들이랑 대외활동 자료 작성 잠깐 하다가 헤어져서 학사 가는 길인데... 너무 피곤하다\n\
    3. 넘졸려서 조금만 자고 과제해야할듯... 진짜피곤하다아악\n\
    4. 저녁먹고 산책나왔다! 기분 좋음\n\
    5. 저녁 먹고 잔깐 산책나왔는데 메가커피 앞에서 사감쌤 마주쳤다! 사감쌤이 먹고싶은 거 사주신다고 얼른 고르래서 박웬수랑 나랑 마카롱 하나 슈크림빵 하나 골랐음... 아껴뒀다 나중에 먹어야지\n\
    \'\'\'"
    start=time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"너는 주어진 문장을 대표할 수 있는 적절한 키워드를 추출하는 assistant야."},
            {"role": "user", "content": f"{text}"}]
        )
    end=time.time()
    print(end-start,'sec')
    output=response.choices[0].message.content
    return output

if __name__ == "__main__":
    user = {
        "userDto": {
            "kakaoId": "101010",
            "username": "민서",
            "age": 23,
            "gender": "여자",
            "job": "대학생"
        },
        "todayStampList": [
            {
                "kakaoId": "101010",
                "dateTime": "2023-06-30T12:00:00",
                "stamp": "피곤",
                "memoLet": "앨리스교수님이 학교에서 343으로 학점 준다고 해서 좀 당황스러움.. 혹시 이번에 A+안주는거 아니겠지 나 좃돼요 안돼.."
            },
            {
                "kakaoId": "101010",
                "dateTime": "2023-06-30T16:00:00",
                "stamp": "우울",
                "memoLet": "다행히 저널은 에이쁠 나옴!"
            },
            {
                "kakaoId": "101010",
                "dateTime": "2023-06-30T22:00:00",
                "stamp": "기쁨",
                "memoLet": "앨리스 교수님이 초대해서 오랜만에 박종훈 선배랑 뵀는데 너무 좋은 시간이었다. 나도 선배님따라 멋진 선배되고싶다.."
            }
        ]
    }
    # 딕셔너리를 JSON으로 변환 
    
    user_data=user.get('userDto')
    prompt=make_prompt(user_data.get('age'),user_data.get('gender'),user_data.get('job'),user.get('todayStampList'))
    print(prompt)
    
    for i in range(3):
        print('-----------',i+1,'회차------------')
        journal,running_time=generate_journal(prompt)
        print(journal)
        print(running_time)



"""
{
    "userDto": {
        "kakaoId": "101010",
        "username": "이민규",
        "age": 22,
        "gender": "남자",
        "job": "대학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "13:12:00",
            "dateTime": "2023-06-25T13:12:00",
            "stamp": "기쁨",
            "memoLet": "점심으로 맛있는 타코야끼와 불닭볶음면을 먹었어요."
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "14:50:00",
            "dateTime": "2023-06-25T14:50:00",
            "stamp": "슬픔",
            "memoLet": "퇴검을 위해 청소하느라 허리가 아파요"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "19:10:00",
            "dateTime": "2023-06-25T19:10:00",
            "stamp": "졸림",
            "memoLet": "드디어 청소가 끝났어요. 저녁으로 배달긱에 새로 생긴 닭강정을 먹었어요. 예상보다 맛있고 양이 많아서 종종 시켜먹어야겠어요."
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "23:03:00",
            "dateTime": "2023-06-25T23:03:00",
            "stamp": "졸림",
            "memoLet": "힘든 하루를 보냈어요"
        }
    ]
}
--------------------------------------------------------------------------------------------------------------------
{
    "userDto": {
        "kakaoId": "101010",
        "username": "민서",
        "age": 23,
        "gender": "여자",
        "job": "대학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "12:04:00",
            "dateTime": "2023-06-25T13:12:00",
            "stamp": "피곤",
            "memoLet": "피곤하지만 일단 포항에 도착했음!!!! 고속버스 4시간 진짜 쉽지않다"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "13:00:00",
            "dateTime": "2023-06-25T14:50:00",
            "stamp": "기쁨",
            "memoLet": "패들보드 너무 재밌었어!!!! 진짜 오랜맘에 해양스포츠 넘 재밌었다"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "18:00:00",
            "dateTime": "2023-06-25T19:10:00",
            "stamp": "우울",
            "memoLet": "너무 걱정했는데 괜찮아 졌다고 하더라도 승재랑 같이 간 곳은 여전히 너무 힘들다 많이 보고싶다"
        },
        {
            "kakaoId": "101010",
            "localDate": "2023-06-25",
            "localTime": "21:00:00",
            "dateTime": "2023-06-25T23:03:00",
            "stamp": "기쁨",
            "memoLet": "꽃돼지식당 돼지고기 존맛진짜..."
        },
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-26T02:03:00",
            "stamp": "기쁨",
            "memoLet": "새벽까지 친구들이랑 술 마시니까 재밌다!"
        }
    ]
}

---------------------------------------------------------------------------------------------------------------------

{
    "userDto": {
        "kakaoId": "101010",
        "username": "민서",
        "age": 23,
        "gender": "여자",
        "job": "대학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T12:00:00",
            "stamp": "피곤",
            "memoLet": "앨리스교수님이 학교에서 343으로 학점 준다고 해서 좀 당황스러움.. 혹시 이번에 A+안주는거 아니겠지 나 좃돼요 안돼.."
        },
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T16:00:00",
            "stamp": "우울",
            "memoLet": "다행히 저널은 에이쁠 나옴!"
        },
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T22:00:00",
            "stamp": "기쁨",
            "memoLet": "앨리스 교수님이 초대해서 오랜만에 박종훈 선배랑 뵀는데 너무 좋은 시간이었다. 나도 선배님따라 멋진 선배되고싶다.."
        }
    ]
}

---------------------------------------------------------------------------------------------------------------------

{
    "userDto": {
        "kakaoId": "101010",
        "username": "민서",
        "age": 23,
        "gender": "여자",
        "job": "대학생"
    },
    "todayStampList": [
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T14:00:00",
            "stamp": "피곤",
            "memoLet": "진짜 영상 학점 미친듯이 짜게줌 미친거아니냐 아.. 그래서 교수님한테 재평가 메일드렷다"
        },
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T15:00:00",
            "stamp": "우울",
            "memoLet": "개열받음 영상 학점 정정해준게 에이제로 아 시발"
        },
        {
            "kakaoId": "101010",
            "dateTime": "2023-06-30T18:00:00",
            "stamp": "기쁨",
            "memoLet": "지원이랑 소하염전이랑 규카츠 먹으러 홍온기 다녀옴 기분 좀 좋아짐"
        }
    ]
}

"""    