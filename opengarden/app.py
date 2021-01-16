# This Python file uses the following encoding: utf-8

from flask import Flask
from flask import request, jsonify, redirect,make_response
import logging
import sqlite3
import json

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/schedule/new', methods=['POST'])
def insertNew():
    logging.info("schedule new")
    logging.info(request)

    logging.info("params")
    params = request.get_json() 

    logging.info(params)

    data={}
    logging.info(f"data  {data}")

    res=saveSchedule(params['date_from'],params['time_from'],params['date_to'],params['time_to'],params['zone_id'],params['status'])
    logging.info(f"res {res.lastrowid}")
    data={"watering_id":res.lastrowid}

    response = make_response(data,200,)
    response.headers["Content-Type"] = "application/json"
    return response


def saveSchedule(date_from,time_from,date_to,time_to,zone_id,status):
    print("save schedule")

    watering_schedule=[(date_from +" " + time_from, date_to+" "+time_to, zone_id, status)]

    conn=getConnection()
    c=conn.cursor()

    c.execute("INSERT INTO watering_schedule(date_from,date_to,zone_id,status) VALUES(?,?,?,?)",(date_from+ " "+time_from,date_to+" "+time_to,zone_id,status))
    conn.commit()
    logging.info("row inserted")
    for row in c:
        logging.info(row)
    return c

def getSchedule(id):
    conn=getConnection()
    c=conn.cursor()
    c.execute("SELECT * FROM watering_schedule WHERE watering_id=?",id)
    
    return c.fetchone()

def getScheduleList(date_from,date_to):
    conn=getConnection()
    c=conn.cursor()
    scheduleList=[]
    data={}
    c.execute("SELECT * FROM watering_schedule WHERE date(date_from)>=? and date(date_to)<=?",(date_from,date_to))
    for row in c:
        logging.info(row)
        data={"date_from":row[0],"date_to":row[1],"zone_id":row[2],"watering_id":row[3],"status":row[4]}
        scheduleList.append(data)
    print(json_serializer(c))
    return scheduleList


def json_serializer(c):
    try :
        columns = []
        result = []
        for column in c.description:
            columns.append(column[0])
        for row in c.fetchall():
            temp_row = dict()
            for key, value in zip(columns, row):
                temp_row[key] = value
                result.append(temp_row)
        return result
    except:
        raise Exception('Invalid cursor provided')

def getConnection():
        conn=None
        try:
            conn=sqlite3.connect('C://repo//openwatering.db')
            #conn=sqlite3.connect('/home/pi/openwatering.db')

        except Error as e:
            print("Couldn't get connection ")
            print(e)

        return conn

#@app.route('/schedule/update', methods=['PUT'])
#def update():


#@app.route('/schedule/delete', methods=['DELETE'])
#def delete():

@app.route('/schedule/list', methods=['GET'])
def list():
    logging.info(request)
    date_from=request.args["date_from"]
    date_to=request.args["date_to"]
    logging.info("schedule list")
    logging.info("params {request.args}")
    res=getScheduleList(date_from,date_to)

    res=jsonify(res)
    logging.info("res")
    logging.info(res)

    response=make_response(res,200,)
    response.headers["Content-Type"] = "application/json"

    return response


app.run()