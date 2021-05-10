from datetime import timedelta
from datetime import datetime
import hashlib
from flask import *

def setCookie(email):
    # set cookie
    expire_time = datetime.now() + timedelta(days=30)  # 30 days expiration
    SECRET_KEY = "ABCABC"
    cookieValue = hashlib.sha256((email + SECRET_KEY).encode('utf-8')).hexdigest()
    print(cookieValue)
    # save cookie to SQL
    # mysql.save_cookie((username, cookieValue))
    resp = make_response(redirect("/"))
    # resp = make_response("SETCOOKIE")
    resp.set_cookie(key="key", value=cookieValue, expires=expire_time, secure=True, httponly=True, samesite=None)
    return resp

def getCookie():
    cookieValue = request.cookies.get("key")
    if cookieValue == None:
        return False
    else:
        return True

def deleteCookie():
    # 刪除cookie & redirect to index.html
    cookieValue = request.cookies.get("key")
    resp = make_response(redirect("/"))
    resp.set_cookie(key="key", value=cookieValue, expires=0, secure=True, httponly=True, samesite=None)
    # delete cookie sql
    # mysql.delete_cookie(cookieValue)
    return resp