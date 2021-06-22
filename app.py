# from Model.api import get_api_attractions, get_api_attractionId,api_internal_error,api_not_found_error, api_not_allowed_error
from Controller.api_user import *
from Controller.api_attraction import *
from Controller.api_booking import *
from Controller.api_orders import *
from Controller.api_board import *
from config import app

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
@app.route("/board")
def board():
	return render_template("board.html")
#Loading
@app.route("/loaderio-55efba7b6dd186cc028922fdc0ed48b6/")
def loading():
	return render_template("loaderio-55efba7b6dd186cc028922fdc0ed48b6.html")


#使用者API
@app.route("/api/user", methods = ["GET","POST","PATCH","DELETE"])
def api_user():
	return get_api_user()

#旅遊景點API
@app.route("/api/attractions", methods = ["GET"])
def api_attractions():
	return get_api_attractions()

@app.route("/api/attraction/<attractionId>", methods = ["GET"])
def api_attractionId(attractionId):
	return get_api_attractionId(attractionId)

#訂單API
@app.route("/api/booking", methods = ["GET","POST","DELETE"])
def api_booking():
	return get_api_booking()

#付款API
@app.route("/api/orders", methods = ["POST"])
def api_orders():
	return get_api_orders()

@app.route("/api/order/<orderNumber>", methods = ["GET"])
def api_orders_number(orderNumber):
	return get_api_orders_number(orderNumber)

#Board API
@app.route("/api/board", methods = ["GET","POST"])
def api_board():
	return api_board_handler()


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

app.run(host="0.0.0.0", port=3000, debug = False)
# app.run(port=3000)
