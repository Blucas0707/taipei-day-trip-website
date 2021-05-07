from Model.api import get_api_attractions, get_api_attractionId,api_internal_error,api_not_found_error, api_not_allowed_error

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
	return get_api_attractions(page,keyword)


@app.route("/api/attraction/<attractionId>", methods = ["GET"])
def api_attractionId(attractionId):
	return get_api_attractionId(attractionId)

#error handle
@app.errorhandler(500)
def internal_error(error):
	return api_internal_error()

@app.errorhandler(404)
def not_found_error(error):
	return api_not_found_error()

@app.errorhandler(403)
def not_allowed_error(error):
	return api_not_allowed_error()

app.run(host="0.0.0.0", port=3000, debug = True)
# app.run(port=3000)