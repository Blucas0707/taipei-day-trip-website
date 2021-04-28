from Model.SQL import SQLDB
import json

#set mysql
mysql = SQLDB()

def get_api_attractions(page,keyword):
    # 防止特殊符號 & SQL injection
    abandom_list = ['"', "'", "%", ";", "="]
    # print(page,keyword)
    for c in str(page):
        if c in abandom_list:
            print("Invalid")
            return render_template("index.html")
    for c in str(keyword):
        if c in abandom_list:
            print("Invalid")
            return render_template("index.html")

    para = (page, keyword)
    # print(para)
    data_dict = mysql.get_api_attractions(page=page, keyword=keyword)
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat

def get_api_attractionId(attractionId):
    data_dict = mysql.get_api_attractionId((attractionId))
    jsonformat = json.dumps(data_dict, sort_keys=False, indent=4)
    return jsonformat


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