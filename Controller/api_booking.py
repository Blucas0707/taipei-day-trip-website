from Model.SQL import SQLDB
import json
import hashlib
from flask import *
from Controller.user_session import *
from dotenv import dotenv_values

#load .env config
config = dotenv_values("../key/.env")

#set mysql
mysql = SQLDB()

#Booking
def get_api_booking(app):
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
        # user email
        email = getSession()["email"]
        # booking data
        data = request.get_json()
        attractionid = data.data.attraction["id"]
        name = data.data.attraction["name"]
        address = data.data.attraction["address"]
        image = data.data.attraction["image"]
        date = data.data["date"]
        time = data.data["time"]
        price = data.data["price"]
        data_dict = {
           "data":{
                "attraction":{
                    "id":attractionid,
                    "name":name,
                    "address":address,
                    "image":image,
                },
                "date":date,
                "time":time,
                "price":price,
           }
        }
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
        email = getSession()["email"]
        #booking data
        data = request.get_json()
        attractionid = data["attractionid"]
        date = str(data["date"])
        time = str(data["time"])
        price = data["price"]
        print(email,attractionid, date, time, price)
        if None in [email,attractionid, date, time, price]:  # null in input
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
        # user email
        data_dict = {
            "ok": True
        }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

