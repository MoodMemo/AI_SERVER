# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:38:23 2023

@author: juLeena
"""

from flask import Flask, request, json, jsonify, send_file, render_template,Response
import openai
import os
from prompt import determine_stamp_type, generate_journal, make_prompt, generate_DR, make_prompt_DR
from statistics import load_db, store_data
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
from io import BytesIO
from time import sleep

import pandas as pd
import numpy as np
from ast import literal_eval

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import chromadb

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)

app = Flask(__name__)
 
plt.rc('font',family='NanumGothic')
matplotlib.rcParams['axes.unicode_minus'] = False

@app.route("/journal", methods=['POST'])
def journal():
    
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
    
    user=params.get('userDto')
    text,time=generate_journal(make_prompt(user.get('age'),user.get('gender'),user.get('job'),params.get('todayStampList')))
    text=text.split(']')
    text2=[text[1].split('[')[0],text[2].split('[')[0],text[3]]
    for i in range(len(text2)):
        text2[i]=text2[i].strip()
    keyword=text2[2].split(',')
    for i in range(len(keyword)):
        keyword[i]=keyword[i].strip()
    
    
    
    d = datetime.datetime.now() - datetime.timedelta(days=1) #어제 날짜로 일기 작성
    date=f'{d.year}-{str(d.month):0>2}-{str(d.day):0>2}'
    temp={"kakaoId":f"{user.get('kakaoId')}",
     "username":f"{user.get('username')}",
     "date":date,
     "title":text2[0],
     "bodyText":text2[1],
     "keyword1st":keyword[0],
     "keyword2nd":keyword[1],
     "keyword3rd":keyword[2],
     "time":f"{time:.2f}"}
    
    #data=json.dumps(temp)
    
    return jsonify(temp)

@app.route("/dailyReport", methods=['POST'])
def dailyReport():
    print('일기 만들라고') 
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
    
    user=params.get('userDto')
    text,time=generate_DR(make_prompt_DR(user.get('age'),user.get('gender'),user.get('job'),params.get('todayStampList')))
    text=text.split(']')
    text2=[text[1].split('[')[0],text[2].split('[')[0],text[3]]
    for i in range(len(text2)):
        text2[i]=text2[i].strip()
    keyword=text2[2].split(',')
    for i in range(len(keyword)):
        keyword[i]=keyword[i].strip()
    
    
    
    date = params.get('today')
    temp={"username":f"{user.get('userName')}",
     "date":date,
     "title":text2[0],
     "bodytext":text2[1],
     "keyword":[keyword[0],keyword[1],keyword[2]],
     "time":f"{time:.2f}"}
    print(temp)
    #data=json.dumps(temp)
    
    return jsonify(temp)

@app.route("/stamp", methods=['POST'])
def stamp():
    params=request.get_json()
    stamp=params.get('stamp')
    result=determine_stamp_type(stamp)
    temp={'result':result}
    
    return jsonify(temp)


def query_collection(collection, query, max_results, dataframe):
    results = collection.query(query_texts=query, n_results=max_results, include=['distances'])
    print(results)
    df = pd.DataFrame({
                'id':results['ids'][0],
                'score':results['distances'][0],
                'content': dataframe[dataframe.vector_id.isin(results['ids'][0])]['text'],
                })

    return df

chroma_db_num=0


@app.route("/stamp_to_mood_report",methods=['POST'])
def stamp_to_mood_report():
    print('stamp to mood report start')
    """
    chroma_client=chromadb.Client()
    params = request.get_json()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL="text-embedding-ada-002"

    embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name=EMBEDDING_MODEL)

    if len(params.get('moodReportEmotions'))==0:
        return jsonify({'result':False,'weekNum':-1})
    check=0
    for index in range(len(params.get('moodReportEmotions'))):
        if params.get('moodReportEmotions')[index][0]!='':
            check=1
    if not check:
        return jsonify({'result':False,'weekNum':-1})

    df = pd.DataFrame(columns=['text','content_vector','vector_id'])

    for index in range(len(params.get('moodReportEmotions'))):
        print(params.get('moodReportEmotions'))
        print(params.get('moodReportEmotions')[index])
        print(params.get('moodReportEmotions')[index][0])

        flag=True

        while flag:
            try:
                response=openai.Embedding.create(model=EMBEDDING_MODEL,input=params.get('moodReportEmotions')[index][0])
                flag=False
            except:
                time.sleep(2)
        df.loc[index]=[params.get('moodReportEmotions')[index][0],str(response["data"][0]["embedding"]),params.get('moodReportEmotions')[index][1]]

    df['content_vector']=df.content_vector.apply(literal_eval)
    df['vector_id'] = df['vector_id'].apply(str)

    collection = chroma_client.create_collection(name=f'mood_report{chroma_db_num}', embedding_function=embedding_function)
    collection.add(ids=df.vector_id.tolist(),
        embeddings=df.content_vector.tolist())

    for stamp in params.get('todayStampList'):

        title_query_result = query_collection(
            collection=collection,
            query=stamp.get('stampName'),
            max_results=1,
            dataframe=df
        )

        if title_query_result.score[0]<0.34:
            chroma_client.delete_collection(name=f'mood_report{chroma_db_num}')
            return jsonify({'result':True,'weekNum':int(title_query_result.id[0])})
    chroma_client.delete_collection(name=f'mood_report{chroma_db_num}')
    """
    return jsonify({'result':False,'weekNum':-1})


@app.route("/draw_daily_stamp_total")
def draw_daily_stamp_total():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    matplotlib.use('agg')

    fig=plt.figure(figsize=(20,15))
    ax=fig.add_subplot(111)
    ax.grid()
    x,y=list(json_object['daily_stamp_total'].keys()),list(json_object['daily_stamp_total'].values())
    ax.set_title("일자 별 총 스탬프 개수(~%s)"%(datetime.datetime.now()))
    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.show()

    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')


@app.route("/draw_time")
def draw_time():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    #print(json_object)
    matplotlib.use('agg')

    fig=plt.figure(figsize=(20,15))
    ax=fig.add_subplot(111)
    ax.grid()
    x,y=list(json_object['stamp_time'].keys()),list(json_object['stamp_time'].values())
    ax.set_title("시간대 별 총 스탬프 개수(~%s)"%(datetime.datetime.now()))
    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.show()


    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/draw_time_daily_stamp_total")
def draw_time_daily_stamp_total():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    matplotlib.use('agg')

    L=[['00','02'],['03','08'],['09','10'],['11','12'],['13','14'],['15','18'],['19','21'],['22','22'],['23','23']]
    fig=plt.figure(figsize=(30,15))
    ax=fig.add_subplot(111)
    ax.grid()
    ax.set_title("일자 별 시간대 스탬프 개수(~%s)"%(datetime.datetime.now()))

    colors=['blue','orange','green','red','purple','pink','brown','gray','olive']
    for i in range(len(L)):
        start=L[i][0]
        end=L[i][1]
        x,y=list(json_object['time_daily_stamp_total'][start+'-'+end].keys()),list(json_object['time_daily_stamp_total'][start+'-'+end].values())
        ax.plot(x,y,color=colors[i],label='%s-%s'%(start,end))
        for pos,data in zip(x,y):
            ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    ax.legend()
    #plt.show()


    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/draw_active_users")
def draw_active_users():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    matplotlib.use('agg')
    #print(json_object)
    fig=plt.figure(figsize=(30,15))
    ax=fig.add_subplot(111)
    #ax.grid()
    ax.set_title("활성 사용자 수(~%s)"%(datetime.datetime.now()))

    keys=list(json_object['active_users'].keys())

    colors=['blue','red','green','purple','gray']
    x=list(json_object['active_users']['1 stamp'].keys())

    for i in range(len(keys)):
        y=list(json_object['active_users'][keys[i]].values())
        ax.plot(x,y,color=colors[i],label=keys[i])
        for pos,data in zip(x,y):
            ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    for pos,data in zip(x,y):
        ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    ax.legend()
    #plt.show()
    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/draw_dailyReport_time")
def draw_dailyReport_time():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    matplotlib.use('agg')
    #print(json_object)
    fig=plt.figure(figsize=(30,15))
    ax=fig.add_subplot(111)
    #ax.grid()
    ax.set_title("일자 별 평균 일기 생성 시간(~%s)"%(datetime.datetime.now()))

    x,y=list(json_object['dailyReport_time'].keys()),list(json_object['dailyReport_time'].values())

    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%.3f'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.legend()
    #plt.show()

    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/draw_avg_daily_stamp")
def draw_avg_daily_stamp():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    matplotlib.use('agg')
    #print(json_object)
    fig=plt.figure(figsize=(30,15))
    ax=fig.add_subplot(111)
    #ax.grid()
    ax.set_title("일자 별 평균 스탬프 개수(~%s)"%(datetime.datetime.now()))

    x,y=list(json_object['daily_stamp_total'].keys()),list(map(lambda x,y:x/y, json_object['daily_stamp_total'].values(), json_object['active_users']['more than 1 stamp'].values()))

    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%.2f'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.legend()
    #plt.show()

    img = BytesIO()
    FigureCanvas(fig).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')
    


@app.route("/statistics/user/<kakaoId>",methods=["GET"])
def user_statistics(kakaoId):
    json_object={"kakaoId":kakaoId,
                 "total_stamp":0,
                 "stamp_by_emotion":{"기쁨😆":0,
                                     "슬픔😭":0,
                                     "우울☹️":0,
                                     "평온🙂":0,
                                     "피곤😴":0,
                                     "기타":0
                                     }
                }
    for item in load_db().stamps.find({"kakaoId": kakaoId}):
        json_object["total_stamp"]+=1
        emotion=item.get('stamp')
        if emotion not in json_object["stamp_by_emotion"]:
            json_object["stamp_by_emotion"]["기타"]+=1
        else:
            json_object["stamp_by_emotion"][emotion]+=1

    return jsonify(json_object)

@app.route("/statistics", methods=["GET"])
def index():
    store_data(load_db())
    return render_template("test.html")


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
