from Model.SQL_order import *
import json
from flask import *
from Controller.user_session import *
from dotenv import dotenv_values
from datetime import datetime

#load .env config
config = dotenv_values("../key/.env")

#ORDER
def get_api_orders():
    if getSession() == False:  # not login
        data_dict = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
    else: #login
        data = request.get_json()
        print(f"ordr data = {data}")
        prime = data["prime"]
        price = data["order"]["price"]
        attractionId = data["order"]["trip"]["attraction"]["id"]
        attractionName = data["order"]["trip"]["attraction"]["name"]
        attractionAddress = data["order"]["trip"]["attraction"]["address"]
        attractionImage = data["order"]["trip"]["attraction"]["image"]
        date = data["order"]["trip"]["date"]
        time = data["order"]["trip"]["time"]
        name = data["order"]["contact"]["name"]
        email = data["order"]["contact"]["email"]
        phone = data["order"]["contact"]["phone"]
        order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        print(order_id)
        para = (prime,price,attractionId,attractionName,attractionAddress,attractionImage,date,time,name,email,phone,order_id)
        #sql
        results = Order().establish_order(para)
        if results == 200: #success
            data_dict = {
              "data": {
                "number": order_id,
                "payment": {
                  "status": 0,
                  "message": "付款成功"
                }
              }
            }
        elif results == 500:
            data_dict = {
                "error": True,
                "message": "Internal Server Error."
            }
        else:
            data_dict = {
                "error": True,
                "message": "訂單建立失敗，輸入不正確或其他原因"
            }

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat


def get_api_orders_number(orderNumber):
    pass

