from flask import Flask, session
from config import app

def setSession(email=None,password=None):
    session["email"] = email
    session["password"] = password
    print("session: ", session.get("email"), session.get("password"))

def removeSession():
    session["email"] = None
    session["password"] = None
    print("session: ", session.get("email"), session.get("password"))

def getSession():
    session_name = session.get("email")
    session_password = session.get("password")
    if session_name != None and session_password != None:
        return (session_name,session_password)
    else:
        return False