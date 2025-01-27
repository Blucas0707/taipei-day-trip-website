from Model.SQL import SQLDB
import json
import hashlib
from flask import *
from dotenv import dotenv_values
from Model.cookie import *

#load .env config
config = dotenv_values("../key/.env")

#set mysql
mysql = SQLDB()

#Error
def api_internal_error():
    data_dict = {
        "error": True,
        "message": "Internal Server Error."
    }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def api_not_found_error():
    data_dict = {
        "error": True,
        "message": "Website not found."
    }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def api_not_allowed_error():
    data_dict = {
        "error": True,
        "message": "Forbidden. Access denied."
    }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat


#USER

def get_api_user(app):
    print(request.method)
    if request.method == "GET":
        return get_user_info_login()
    elif request.method == "POST":
        return user_info_register()
    elif request.method == "PATCH":
        return user_info_login()
    else:
        return user_info_logout()

def get_user_info_login():
    print(session.get("email"))
    if session.get("email") != None and session.get("password") != None:
        email = session.get("email")
        password = session.get("password")
        para = (email,password)
        results = mysql.checkLogin(para)
        data_dict = {
            "data": {
                "id": results[1],
                "name": results[2],
                "email": result[3]
            }
        }
    else:
        data_dict = None
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def user_info_register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = passwordEncrypt(str(data["password"]))  # password 加密
    # print(name,email, password)
    if None in [email, password]:  # null in input
        data_dict = {
            "error": True,
            "message": "輸入為空，請重新輸入"
        }
    else:
        para = (name, email, password)
        success = mysql.user_register(para)
        # print(success)
    if success == 200:
        data_dict = {
            "ok": True
        }
    elif success == 400:
        data_dict = {
            "error": True,
            "message": "註冊失敗，重複的 Email 或其他原因"
        }
    else:
        return api_internal_error()

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    # print(jsonformat)
    return jsonformat

def user_info_login():
    data = request.get_json()
    email = data["email"]
    password = passwordEncrypt(str(data["password"]))  # password 加密
    print("#01" ,email, password)
    if None in [email,password]: #null in input
        data_dict = {
            "error": True,
            "message": "輸入為空，請重新輸入"
        }
    else:
        para = (email,password)
        success = mysql.user_login(para)

    if success == 200: #login success
        usersession.setSession(email,password)
        data_dict = {
          "ok": True
        }
    elif success == 400:
        data_dict = {
            "error": True,
            "message": "登入失敗，Email/密碼錯誤"
        }
    else:
        return api_internal_error()

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    print(success, jsonformat)
    return jsonformat

def user_info_logout():
    session["email"] = None
    session["password"] = None
    data_dict = {
        "ok": True
    }
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def passwordEncrypt(password):
    SECRET_KEY = config["SQL_PWD_ENCRYPT_SECRET_KEY"]
    new_password = hashlib.sha256((password + SECRET_KEY).encode('utf-8')).hexdigest()
    return new_password
