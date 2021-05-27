from Model.SQL import *

class Order(SQLDB):
    def establish_order(self, para =None):
        try:
            sql = """insert into taipei_travel_orders (order_number,order_unpaid,price,attraction_id,
                    attraction_name,attraction_address,attraction_image,date,time,name,email,phone)  
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            con.commit()
            # close sql connect
            self.close(cursor, con)
            return 200
        except:
            #rollback DB
            con.rollback()
            return 500

    def update_payment(self,para =None):
        try:
            print(para)
            sql = """update taipei_travel_orders set order_unpaid = 0 where order_number = %s """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            con.commit()
            print("update success")
            # close sql connect
            self.close(cursor, con)
            return 200
        except:
            #rollback DB
            con.rollback()
            return 500

    def get_order(self, para=None):
        try:
            sql = """select * from taipei_travel_orders where order_number = %s """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            result = cursor.fetchone()
            # close sql connect
            self.close(cursor, con)

            if result != None: #exist
                data_dict = {
                  "data": {
                    "number": "",
                    "price": -1,
                    "trip": {
                      "attraction": {
                        "id": -1,
                        "name": "",
                        "address": "",
                        "image": ""
                      },
                      "date": "",
                      "time": ""
                    },
                    "contact": {
                      "name": "",
                      "email": "",
                      "phone": ""
                    },
                    "status": -1
                  }
                }
                #set data
                data_dict["data"]["number"] = result[1]
                data_dict["data"]["price"] = result[3]
                data_dict["data"]["trip"]["attraction"]["id"] = result[4]
                data_dict["data"]["trip"]["attraction"]["name"] = result[5]
                data_dict["data"]["trip"]["attraction"]["address"] = result[6]
                data_dict["data"]["trip"]["attraction"]["image"] = result[7]
                data_dict["data"]["trip"]["date"] = result[8]
                data_dict["data"]["trip"]["time"] = result[9]
                data_dict["data"]["contact"]["name"] = result[10]
                data_dict["data"]["contact"]["email"] = result[11]
                data_dict["data"]["contact"]["phone"] = result[12]
                data_dict["data"]["status"] = result[2]

                if data_dict["data"]["status"] == 1: #unpaid
                    data_dict = None
                print(f"data_dict = {data_dict}")
            else: #not exist
                data_dict = None
            return data_dict
        except:
            return 500