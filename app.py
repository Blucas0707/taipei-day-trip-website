from SQL import SQLDB
import json

#set mysql
mysql = SQLDB()

from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



#旅遊景點API
@app.route("/api/attractions", methods = ["GET"])
def api_attractions():
	#get page & keyword variables
	page = 0 if not request.args.get("page") else int(request.args.get("page"))
	keyword = "" if not request.args.get("keyword") else request.args.get("keyword")
	para = (page,keyword)
	data_dict = mysql.get_api_attractions(page = page, keyword = keyword)
	jsonformat = json.dumps(data_dict, sort_keys=False, indent = 4)
	return jsonformat


@app.route("/api/attraction/<attractionId>", methods = ["GET"])
def api_attractionId(attractionId):
	#get data from sql
	result = mysql.get_api_attractionId((attractionId))
	#return to web
	return json.dumps(result, sort_keys=False, indent = 4)

#error handle
@app.errorhandler(500)
def internal_error(error):
	data_dict = {
		"error": True,
  		"message": "Internal Server Error."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)

@app.errorhandler(404)
def not_found_error(error):
	data_dict = {
		"error": True,
  		"message": "Website not found."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)

@app.errorhandler(403)
def not_found_error(error):
	data_dict = {
		"error": True,
  		"message": "Forbidden. Access denied."
	}
	return json.dumps(data_dict, sort_keys= False, indent= 4)
app.run(host="0.0.0.0", port=3000)
# app.run(port=3000)