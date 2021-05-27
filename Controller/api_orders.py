from Model.SQL_order import *
from Controller.api_tappay import *
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
        print(f"order data = {data}")
        order_number = datetime.now().strftime("%Y%m%d%H%M%S")    #訂單編號
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

        # save into SQL
        order_unpaid = 1 # unpaid
        para = (
            order_number, order_unpaid , price, attractionId, attractionName, attractionAddress, attractionImage, date, time, name,
            email,phone)
        # sql
        results = Order().establish_order(para)

        #Tappay
        tappay = TapPay(data)
        pay_result = tappay.Pay()
        if pay_result: # success
            data_dict = {
              "data": {
                "number": order_number,
                "payment": {
                  "status": 0,
                  "message": "付款成功"
                }
              }
            }
            #UPDATE SQL
            para = (str(order_number),)
            # sql
            results = Order().update_payment(para)
            print(f"UPDATE:{results}")
            if results == 500:
                data_dict = {
                    "error": True,
                    "message": "伺服器內部錯誤"
                }
        else: #pay fail
            data_dict = {
                "error": True,
                "message": "訂單建立失敗，輸入不正確或其他原因"
            }

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat


def get_api_orders_number(orderNumber):
    if getSession() == False:  # not login
        data_dict = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
    else:  # login
        para = (str(orderNumber),)
        result = Order().get_order(para)
        if result == 500:
            data_dict = {
                "error": True,
                "message": "伺服器內部錯誤"
            }

    jsonformat = json.dumps(result, indent=4, sort_keys=False)
    return jsonformat

