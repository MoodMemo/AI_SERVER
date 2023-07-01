# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:38:23 2023

@author: juLeena
"""

from flask import Flask, request, json, jsonify, send_file, render_template,Response
import openai
import os
from prompt import generate_journal, generate_keyword, make_prompt
from statistics import load_db, store_data
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
from io import BytesIO
from time import sleep

app = Flask(__name__)

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







@app.route("/draw_daily_stamp_total")
def draw_daily_stamp_total():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    
    sleep(0.1)
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    ax.grid()
    x,y=list(json_object['daily_stamp_total'].keys()),list(json_object['daily_stamp_total'].values())
    ax.set_title("Total Daily Stamp(~%s)"%(datetime.datetime.now()))
    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.show()
    
    img = BytesIO()
    FigureCanvas(plt.gcf()).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')


@app.route("/draw_time")
def draw_time():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    #print(json_object)
    sleep(0.1)
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    ax.grid()
    x,y=list(json_object['stamp_time'].keys()),list(json_object['stamp_time'].values())
    ax.set_title("Total Stamp time(~%s)"%(datetime.datetime.now()))
    ax.plot(x,y,color="blue")
    for pos,data in zip(x,y):
        ax.annotate('%s'%data,xy=(pos,data),textcoords='data',fontsize=13)
    #plt.show()


    img = BytesIO()
    FigureCanvas(plt.gcf()).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/draw_time_daily_stamp_total")
def draw_time_daily_stamp_total():
    with open("index.json","r") as file:
        json_object=eval(json.load(file))
    
    sleep(0.1)
    L=[['00','02'],['03','08'],['09','10'],['11','12'],['13','14'],['15','18'],['19','21'],['22','22'],['23','23']]
    fig=plt.figure(figsize=(12,12))
    ax=fig.add_subplot(111)
    ax.grid()
    ax.set_title("Total Stamp time(~%s)"%(datetime.datetime.now()))
    
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
    FigureCanvas(plt.gcf()).print_png(img)
    #plt.savefig(img, format='png', dpi=200)
    #img.seek(0)
    #return send_file(img, mimetype='image/png')
    return Response(img.getvalue(), mimetype='image/png')



@app.route("/statistics", methods=["GET"])
def index():
    return render_template("test.html")



"""
@app.route("/keyword", methods=['POST'])
def keyword():
    
    params = request.get_json()

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

    
    user=params.get('userDto')
    text,time=generate_journal(user.get('age'),user.get('gender'),user.get('job'),params.get('todayStampList'))
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
     "keyword":keyword,
     "time":f"{time:.2f}"}
    
    data=json.dumps(temp)
    
    return data
"""

if __name__ == '__main__':
    store_data(load_db())
    app.run('0.0.0.0',port=5000,debug=True)