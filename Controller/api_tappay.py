import json
from dotenv import dotenv_values
import requests

#load .env config
config = dotenv_values("../key/.env")


class TapPay:
    def __init__(self,data):
        self.data = data
        self.url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime" #test url

    def Pay(self):
        prime = self.data["prime"]
        price = self.data["order"]["price"]
        detail = self.data["order"]["trip"]["date"] + "," + self.data["order"]["trip"]["time"] + "," + self.data["order"]["trip"]["attraction"]["name"]
        phone = self.data["order"]["contact"]["phone"]
        name = self.data["order"]["contact"]["name"]
        email = self.data["order"]["contact"]["email"]
        data = {
          "prime": prime,
          "partner_key": config["TAPPAY_partner_key"],
          "merchant_id": config["TAPPAY_merchant_id"],
          "details": detail,
          "amount": price,
          "cardholder": {
              "phone_number": phone,
              "name": name,
              "email": email,
          },
          "remember": False
        }
        print(data)
        encoded_body = json.dumps(data)
        my_headers = {
            'Content-Type': 'application/json',
            "x-api-key": config["TAPPAY_partner_key"]
        }

        req = requests.post(url = self.url,
                 headers=my_headers,
                 data=encoded_body)

        print(req.json())
        status = req.json()["status"]
        if status == 0: #success
            return True
        else:
            return False