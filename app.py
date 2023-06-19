# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:38:23 2023

@author: juLeena
"""

from flask import Flask, request, json, jsonify
import openai
import os
from prompt import generate_journal
import json
import datetime

app = Flask(__name__)

@app.route("/test", methods=['POST'])
def test():
    
    params = request.get_json()
    """
    #print("Json :", params)
    name=params.get('name')
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content":f"{name}이 뭐지?"}]
        )
    #end=time.time()
    #print(end-start,'sec')
    output=response.choices[0].message.content
    #print(output)
    data = {
        "result": f"{output}"
    }
    #print(output)
    """
    
    text=generate_journal()
    text=text.split(']')
    text2=[text[1].split('[')[0],text[2].split('[')[0],text[3]]
    for i in range(len(text2)):
        text2[i]=text2[i].strip()
    keyword=text2[2].split(',')
    for i in range(len(keyword)):
        keyword[i]=keyword[i].strip()
    
    
    
    d = datetime.datetime.now() - datetime.timedelta(days=1) #어제 날짜로 일기 작성
    date=f'{d.year}-{str(d.month):0>2}-{str(d.day):0>2}'
    temp={"kakaoId":f"{params.get('kakaoId')}",
     "username":f"{params.get('username')}",
     "date":date,
     "title":text2[0],
     "bodyText":text2[1],
     "keyword":keyword}
    
    data=json.dumps(temp)
    
    return data

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)