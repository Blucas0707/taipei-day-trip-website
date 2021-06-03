from Model.SQL import SQLDB
import json
from datetime import datetime
from flask import *
from Controller.user_session import *
from dotenv import dotenv_values

#load .env config
config = dotenv_values("../key/.env")

#set mysql
mysql = SQLDB()

#Booking
def get_api_booking():
    print(request.method)
    if request.method == "GET":
        return get_booking_info()
    elif request.method == "POST":
        return establish_booking_info()
    else:
        return delete_booking_info()

def get_booking_info():
    if getSession() == False:  # not login
        data_dict = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
    else:  # Login
        email = getSession()[0] # user email
        results = mysql.get_booking((email,))
        if results != None:
            # print(f"results={results}")
            attractionId = results[0]
            name = results[1]
            address = results[2]
            image = results[3]
            date = results[4]
            time = results[5]
            price = results[6]

            data_dict = {
               "data":{
                    "attraction":{
                        "id":attractionId,
                        "name":name,
                        "address":address,
                        "image":image,
                    },
                    "date":date,
                    "time":time,
                    "price":price,
               }
            }
        else:
            data_dict = None
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    # print(f"json:{jsonformat}")
    return jsonformat

def establish_booking_info():
    if getSession() == False: #not login
        data_dict = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
    else: #Login
        # user email
        email = getSession()[0]
        #booking data
        data = request.get_json()
        print(data)
        attractionid = data["attractionId"]
        date = str(data["date"])
        time = str(data["time"])
        price = data["price"]
        print(email,attractionid, date, time, price)
        if None in [email,attractionid, date, time, price]:  # null in input
            data_dict = {
                "error": True,
                "message": "輸入不正確，請重新輸入"
            }
        elif date < datetime.now().strftime("%Y-%m-%d"):
            #date < now
            data_dict = {
                "error": True,
                "message": "輸入不正確，請重新輸入"
            }
        else:
            para = (email,attractionid, date, time, price)
            success = mysql.establish_booking(para)
            # print(success)
            if success == 200:
                data_dict = {
                    "ok": True
                }
            elif success == 500:
                data_dict = {
                    "error": True,
                    "message": "伺服器內部錯誤"
                }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    # print(jsonformat)
    return jsonformat

def delete_booking_info():
    if getSession() == False:  # not login
        data_dict = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
    else:  # Login
        # print(f"Session:{getSession()}")
        email = getSession()[0] #email
        # print(f"email: {email}")
        #delete booking data
        result = mysql.delete_booking((email,))
        if result == 200:
            data_dict = {
                "ok": True
            }
        else:
            data_dict = {
                "error": True,
                "message": "Internal Server Error."
            }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

