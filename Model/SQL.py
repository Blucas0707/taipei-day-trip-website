import mysql.connector
import mysql.connector.pooling
from dotenv import dotenv_values

#load .env config
config = dotenv_values("../key/.env")

class SQLDB:
    def __init__(self):
        self.config = {
            "host":config["SQL_HOST"],
            "database":config["SQL_DATABASE"],
            "user":config["SQL_USER"],
            "password":config["SQL_PASSWORD"],
            "auth_plugin":"mysql_native_password"
        }
        self.pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",pool_size = 8,pool_reset_session=True,**self.config)
        # self.conn = self.pool.get_connection()
        print("POOL連線成功")
    def close(self,cursor ,con):
        cursor.close()
        con.close()

    # def Update(self, para= None):
    #     sql = "REPLACE INTO taipei_travel_info (id, name, category, description, address, transport, mrt, latitude, longitude) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
    #     cursor = self.conn.cursor()
    #     cursor.execute(sql, para)
    #     self.conn.commit()
    #
    # def save_image_link(self, para = None):
    #     cursor = self.conn.cursor()
    #     #link existed or not
    #     sql = "select count(*) from taipei_travel_images where link = '%s'"
    #     cursor.execute(sql, para[1])
    #     result = cursor.fetchone()
    #     #link not existed
    #     if result[0] == 0:
    #         sql = "INSERT INTO taipei_travel_images (id, link) VALUES ('%s', '%s')"
    #         cursor.execute(sql, para)
    #         self.conn.commit()
    #     else:
    #         return False

    def get_api_attractionId(self, para = None):
        #judge id include invalid character
        try:
            data_dict = {}
            con = self.pool.get_connection()
            cursor = con.cursor()
            sql = "select * from taipei_travel_info where id = %s limit 1"
            cursor.execute(sql, (para,))
            results = cursor.fetchall()
            # judge id not in sql
            if len(results) == 0:
                data_dict = {
                    "error": True,
                    "message": "id not existed"
                }
            else:
                #id existed
                data_dict = {
                    "data": {
                    }
                }
                for result in results:
                    # print(result)
                    data_dict["data"]["id"] = result[0]
                    data_dict["data"]["name"] = result[1]
                    data_dict["data"]["category"] = result[2]
                    data_dict["data"]["description"] = result[3]
                    data_dict["data"]["address"] = result[4]
                    data_dict["data"]["transport"] = result[5]
                    data_dict["data"]["mrt"] = result[6]
                    data_dict["data"]["latitude"] = float(result[7])
                    data_dict["data"]["longitude"] = float(result[8])

                # get image link
                sql = "select link from taipei_travel_images where id = %s "
                cursor.execute(sql, (para,))
                results = cursor.fetchall()
                image_links = []
                for result in results:
                    image_links.append(result[0])
                data_dict["data"]["images"] = image_links
                #close sql connect
                self.close(cursor,con)

        except:
            data_dict = {
                "error": True,
                "message": "Internal server error"
            }
        finally:
            return data_dict

    def get_api_attractions(self,page = None, keyword = None):
        next_page = page + 1
        offset = page * 12
        data_dict = {
            "nextPage": next_page,
            "data":[]
        }
        con = self.pool.get_connection()
        cursor = con.cursor()
        if keyword == "":
            sql = "select * from (select * from taipei_travel_info order by id) as T limit %s,12"
            para = (offset,)
        else:
            sql = "select * from (select * from taipei_travel_info order by id)as T where name like %s limit %s,12"
            para = ("%"+keyword+"%", offset)
        cursor.execute(sql,para)
        results = cursor.fetchall()

        #no further data
        if len(results) == 0:
            data_dict["nextPage"] = None
            data_dict["data"] = None
        else:
            for result in results:
                new_dict = {}
                new_dict["id"] = result[0]
                new_dict["name"] = result[1]
                new_dict["category"] = result[2]
                new_dict["description"] = result[3]
                new_dict["address"] = result[4]
                new_dict["transport"] = result[5]
                new_dict["mrt"] = result[6]
                new_dict["latitude"] = float(result[7])
                new_dict["longitude"] = float(result[8])
                # get image link
                sql = "select link from taipei_travel_images where id = '%s'"
                cursor.execute(sql, (new_dict["id"],))
                results = cursor.fetchall()
                image_links = []
                for result in results:
                    image_links.append(result[0])

                new_dict["images"] = image_links
                data_dict["data"].append(new_dict)
        # close sql connect
        self.close(cursor, con)
        return data_dict

    #USER
    def user_register(self, para =None ):
        # user existed
        sql = """select count(*) from taipei_travel_user_info where email = %s limit 1 """
        email = para[1] #email
        con = self.pool.get_connection()
        cursor = con.cursor()
        cursor.execute(sql,(email,))
        result = cursor.fetchone()

        if result[0] == 0: #user not existed
            try:
                sql = """insert into taipei_travel_user_info (name,email,password)  values (%s,%s,%s)"""
                cursor.execute(sql, para)
                con.commit()
                # close sql connect
                self.close(cursor, con)
                return 200
            except:
                return 500
        else:
           return 400


    def user_login(self, para =None):
        # user existed
        try:
            sql = """select count(*) from taipei_travel_user_info where email = %s and password = %s """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            result = cursor.fetchone()
            # close sql connect
            self.close(cursor, con)
            if result[0] == 1:  # user info match
                return 200
            else:
                return 400
        except:
            return 500

    def checkLogin(self, para =None):
        #check user login

        sql = """select * from taipei_travel_user_info where email = %s and password = %s limit 1 """
        con = self.pool.get_connection()
        cursor = con.cursor()
        cursor.execute(sql, para)
        results = cursor.fetchone()

        # close sql connect
        self.close(cursor, con)
        return results

    #Booking
    def establish_booking(self, para =None):
        try:
            sql = """insert into taipei_travel_booking (email,attractionId,date,time,price)  values (%s,%s,%s,%s,%s)"""
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            con.commit()
            # close sql connect
            self.close(cursor, con)
            return 200
        except:
            return 500





