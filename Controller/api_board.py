from Model.RDS_SQL import *
from Model.AWS_S3 import *
from werkzeug.utils import secure_filename
import json
import hashlib
from flask import *
from Controller.user_session import *
from dotenv import dotenv_values

#load .env config
config = dotenv_values("../key/.env")

RDS = RDS_SQLDB()

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
def api_board_handler():
    print(request.method)
    if request.method == "GET":
        return get_board_info()
    elif request.method == "POST":
        return post_board_info()

def get_board_info():
    try:
        data_dict = RDS.getData()
    except:
        data_dict = {
            "error": True,
            "message": "get data fail"
        }

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def post_board_info():
    data = request.form
    print(data)
    text = str(data["comment"])
    # print(data, text)
    img = request.files["img"]
    print(img,img.filename)

    if img and allowed_file(img.filename):  # file exists and allowed img (.jpg, png)
        filename = secure_filename(img.filename)
        print(img.filename)
        print(filename)
        img.save(filename)
        FOLDER_NAME = "img/"
        try:
            s3.upload_file(
                Bucket=config["S3_BUCKET_NAME"],
                Filename=filename,
                Key=FOLDER_NAME + filename
            )
            print("Upload Done!")
        except:
            print("Upload Fail!")

        print("Ready to save in RDS")
        cloudfront = config["AWS_CLOUDFRONT"]
        img_link = cloudfront + FOLDER_NAME + filename
        para = (text, img_link)
        print(f"para: {para}")
        results = RDS.upload(para = para)
        print(f"results: {results}")
        data_dict = {
            "comment":results[1],
            "img_link":results[2]
        }

    else:
        data_dict = {
            "error": True,
            "message": "file format error."
        }

    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    print(filename.rsplit('.', 1)[1].lower())
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def passwordEncrypt(password):
    SECRET_KEY = config["SQL_PWD_ENCRYPT_SECRET_KEY"]
    new_password = hashlib.sha256((password + SECRET_KEY).encode('utf-8')).hexdigest()
    return new_password
