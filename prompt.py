# -*- coding: utf-8 -*-

import openai
import os
#import datetime
import time
import tiktoken
#import json
#import requests




def generate_journal(age,gender,job,memolet_list):
    #d = datetime.datetime.now() - datetime.timedelta(days=1) #어제 날짜로 일기 작성
    #date=f'{str(d.year%100):0>2}.{str(d.month):0>2}.{str(d.day):0>2}'
    #week=['월','화','수','목','금','토','일']
    #weekday=week[d.weekday()]
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    let=''
    for i in range(len(memolet_list)):
        let+=f"{i+1}. {memolet_list[i].get('memoLet')}\n"
    text=f"너는 {age}세 {gender} {job}의 입장에서 주어진 조건에 따라 일기를 작성해주는 assistant야.\n아래 '''로 구분된 내용을 합쳐 하나의 일기를 써줘.\n이때 일기에는 [제목], [내용], [키워드]가 포함되도록 해줘.\n\'\'\'\n{let}\'\'\'"
    #print(text)
    
    start=time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content":f"{text}"}]
        )
    end=time.time()
    #print(end-start,'sec')
    """
    print(response.usage)
    output=response.choices[0].message.content
    print(output)
    """
    
    return response.choices[0].message.content, end-start

if __name__ == "__main__":
    print(generate_journal())




"""
text=f"아래 '''로 구분된 내용으로 일기를 써줘.\n\n\
\'\'\'\n\
1. 과제... 할 건 많은데 막상 과제 하러 들어가면 뭐부터 손대야 할지 감이 안 온다. 그래도 제일 어려운 부분 오늘 끝내서 내일이면 얼추 완성시킬 수 있을 것 같다\n\
2. 점심으로 친구들이랑 초밥 먹었다 맛은 그냥 무난! 지금 밥 다 먹고 친구들이랑 대외활동 자료 작성 잠깐 하다가 헤어져서 학사 가는 길인데... 너무 피곤하다\n\
3. 넘졸려서 조금만 자고 과제해야할듯... 진짜피곤하다아악\n\
4. 저녁먹고 산책나왔다! 기분 좋음\n\
5. 저녁 먹고 잔깐 산책나왔는데 메가커피 앞에서 사감쌤 마주쳤다! 사감쌤이 먹고싶은 거 사주신다고 얼른 고르래서 박웬수랑 나랑 마카롱 하나 슈크림빵 하나 골랐음... 아껴뒀다 나중에 먹어야지\n\
\'\'\'"


#start=time.time()
openai.api_key = os.getenv("OPENAI_API_KEY") 
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": f"너는 {user.get('age')}세 {user.get('sex')} {user.get('job')}의 입장에서 주어진 조건에 따라 일기를 작성해주는 assistant야."},
        {"role": "user", "content":f"{text}"}]
    )
#end=time.time()
#print(end-start,'sec')
print(response.usage)
output=response.choices[0].message.content
print(output)
"""

"""
text=f"{output}\n\
위 글을 아래 '''로 구분된 내용의 문체,  말어미, 사용된 단어의 수준, ..., ㅠㅠ와 같은 이모티콘 혹은 인터넷 축약어의 사용 빈도 등을 분석한 후, 네가 방금 작성한 일기를 분석한 스타일대로 수정해줘. 이때 1. 2. 3. 처럼 나열되는 형식은 스타일 분석에서 제외해. 그리고 일기만 출력해줘.\n\
\'\'\'\n\
1. 과제... 할 건 많은데 막상 과제 하러 들어가면 뭐부터 손대야 할지 감이 안 온다. 그래도 제일 어려운 부분 오늘 끝내서 내일이면 얼추 완성시킬 수 있을 것 같다\n\
2. 점심으로 친구들이랑 초밥 먹었다 맛은 그냥 무난! 지금 밥 다 먹고 친구들이랑 대외활동 자료 작성 잠깐 하다가 헤어져서 학사 가는 길인데... 너무 피곤하다\n\
3. 넘졸려서 조금만 자고 과제해야할듯... 진짜피곤하다아악\n\
4. 저녁먹고 산책나왔다! 기분 좋음\n\
5. 저녁 먹고 잔깐 산책나왔는데 메가커피 앞에서 사감쌤 마주쳤다! 사감쌤이 먹고싶은 거 사주신다고 얼른 고르래서 박웬수랑 나랑 마카롱 하나 슈크림빵 하나 골랐음... 아껴뒀다 나중에 먹어야지\n\
\'\'\'"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": f"너는 {user.get('age')}세 {user.get('sex')} {user.get('job')}의 입장에서 주어진 조건에 따라 일기를 쓰는 assistant야."},
        {"role": "user", "content":f"{text}"}]
    )

print(response.usage)
output=response.choices[0].message.content
print(output)

print(text)
print('토큰 개수 :',len(tokenizer.encode(text)),'개')
print('------------------------------------')
print(output)

print('======================================')

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
print(text)
print('토큰 개수 :',len(tokenizer.encode(text)),'개')
print('------------------------------------')
print(output)


"""
"""
userID=1
name="이준하"
userType="22세/남자/대학생"
d = datetime.datetime.now() - datetime.timedelta(days=1) #어제 날짜로 일기 작성
date=f'{d.year}-{str(d.month):0>2}-{str(d.day):0>2}'
title=""
bodyText=""
noc=0
keyword=[]

temp = {
    "userId":f"{userID}",
    "name": name,
    "date": date,
    "title": title,
    "bodyText": bodyText,
    "keyword": keyword
}

url = "http://1.2.3.4"

# headers
headers = {
    "Content-Type": f"api/dailyReport/{userID}"
}

data = json.dumps(temp)

# 변환된 Data를 보내고자 하는 URL에 보내기
response = requests.post(url, headers=headers, data=data)

# 송신 결과 확인
print("response: ", response)
print("response.text: ", response.text)
"""