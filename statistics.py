# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 01:07:53 2023

@author: juLeena
"""
import datetime
import pymongo
import json
import dotenv
import os

def load_db():
    #dotenv.load_dotenv()

    client = pymongo.MongoClient(os.getenv("mongoUrl"))

    db=client.get_database("moodmemo")

    return db

def store_data(db):
    #prev_time=datetime.datetime(2023, 6, 23)
    prev_time=datetime.datetime(2023, 7, 8)
    #DR_start_time=datetime.datetime(2023, 6, 27)
    DR_start_time=datetime.datetime(2023, 7, 8)
    now_time=datetime.datetime.now()
    pres_time=now_time - datetime.timedelta(hours=9) #UTC로 변경
    #print(pres_time)
    json_object={
                'daily_stamp_total':{},
                'stamp_time':{},
                'time_daily_stamp_total':{
                                            '00-02':{},
                                            '03-08':{},
                                            '09-10':{},
                                            '11-12':{},
                                            '13-14':{},
                                            '15-18':{},
                                            '19-21':{},
                                            '22-22':{},
                                            '23-23':{}
                                        },
                'active_users':{'1 stamp':{'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((now_time-prev_time).days+1)},
                                '2 stamps':{'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((now_time-prev_time).days+1)},
                                'more than 1 stamp':{'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((now_time-prev_time).days+1)},
                                'more than 2 stamps':{'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((now_time-prev_time).days+1)},
                                'more than 3 stamps':{'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((now_time-prev_time).days+1)}},
                'dailyReport_time':{'%s'%(DR_start_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range(1,(now_time-DR_start_time).days)}
                }
    #start storing total daily stamp
    for item in db.stamps.find({"dateTime":{"$gt":prev_time,"$lte":pres_time}}):
        stamp_time=(item['dateTime']+datetime.timedelta(hours=9)).strftime("%m-%d")
        if stamp_time not in json_object['daily_stamp_total']:
            json_object['daily_stamp_total'][stamp_time]=1
        else:
            json_object['daily_stamp_total'][stamp_time]+=1
    #end storing total daily stamp

    #start storing stamp_time
    for item in db.stamps.find({"dateTime":{"$gt":prev_time,"$lte":pres_time}}):
        stamp_time=(item['dateTime']+datetime.timedelta(hours=9)).strftime("%H")
        if stamp_time not in json_object['stamp_time']:
            json_object['stamp_time'][stamp_time]=1
        else:
            json_object['stamp_time'][stamp_time]+=1
    #end storing stamp_time

    #start storing time_daily_stamp_total
    L=[['00','02'],['03','08'],['09','10'],['11','12'],['13','14'],['15','18'],['19','21'],['22','22'],['23','23']]
    for i in range(len(L)):
        start=L[i][0]
        end=L[i][1]
        json_object2={'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):0 for i in range((pres_time+datetime.timedelta(hours=9)-prev_time).days+1)}
        for item in db.stamps.find({"dateTime":{"$gt":prev_time,"$lte":pres_time}}):
            stamp_date=(item['dateTime']+datetime.timedelta(hours=9)).strftime("%m-%d")
            stamp_time=(item['dateTime']+datetime.timedelta(hours=9)).strftime("%H")
            if start<=stamp_time<=end:
                json_object2[stamp_date]+=1
        json_object['time_daily_stamp_total'][start+'-'+end]=json_object2
    #end storing time_daily_stamp_total

    #start storing active_users
    active_users_hash={'%s'%(prev_time+datetime.timedelta(days=i)).strftime("%m-%d"):{} for i in range((now_time-prev_time).days+1)}
    for item in db.stamps.find({"dateTime":{"$gt":prev_time,"$lte":pres_time}}):
        stamp_date=(item['dateTime']+datetime.timedelta(hours=9)).strftime("%m-%d")
        user_kakaoId=item['kakaoId']
        if user_kakaoId not in active_users_hash[stamp_date]:
            active_users_hash[stamp_date][user_kakaoId]=1
            json_object['active_users']['1 stamp'][stamp_date]+=1
            json_object['active_users']['more than 1 stamp'][stamp_date]+=1
        else:
            active_users_hash[stamp_date][user_kakaoId]+=1
            if active_users_hash[stamp_date][user_kakaoId]==2:
                json_object['active_users']['1 stamp'][stamp_date]-=1
                json_object['active_users']['2 stamps'][stamp_date]+=1
                json_object['active_users']['more than 2 stamps'][stamp_date]+=1
            elif active_users_hash[stamp_date][user_kakaoId]==3:
                json_object['active_users']['2 stamps'][stamp_date]-=1
                json_object['active_users']['more than 3 stamps'][stamp_date]+=1
    #end storing active_users
    """
    #start storing dailyReport_time
    for item in db.dailyReport.find({"date":{"$gt":DR_start_time,"$lte":now_time}}):
        DR_date=(item['date']+datetime.timedelta(hours=9)).strftime("%m-%d")
        json_object['dailyReport_time'][DR_date]+=float(item['time'])
    for key in json_object['dailyReport_time'].keys():
        json_object['dailyReport_time'][key]/=json_object['active_users']['more than 2 stamps'][key]
    #end storing dailyReport_time
    """
    #TODO : 그 외 다른 통계들 추가하기

    json_object2 = json.dumps(json_object,sort_keys=True, default=str)
    with open('index.json', 'w') as f:
        json.dump(json_object2, f)
