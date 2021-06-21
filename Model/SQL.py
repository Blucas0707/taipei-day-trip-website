import mysql.connector
from mysql.connector import pooling
from dotenv import dotenv_values
import json
#load .env config
config = dotenv_values("../key/.env")

class SQLDB:
    def __init__(self):
        self.config = {
            "host": config["RDS_SQL_HOST"],
            "database": json.loads(config["RDS_SQL_DATABASE"])["travel"],
            "port": config["RDS_SQL_PORT"],
            "user": config["RDS_SQL_USER"],
            "password": config["RDS_SQL_PASSWORD"],
            "auth_plugin": "mysql_native_password"
        }
        self.pool = pooling.MySQLConnectionPool(pool_name = "SQLpool",pool_size = 8,pool_reset_session=True,**self.config)
        self.conn = self.pool.get_connection()
        print("Connection Pool Name - ", self.pool.pool_name)
        print("Connection Pool Size - ", self.pool.pool_size)
        print("POOL連線成功-travel")

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
                con.close()

        except:
            # rollback DB
            con.rollback()
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
        # pcon = pooling.PooledMySQLConnection(self.pool,self.conn)
        # con = self.pool.get_connection()
        cursor = con.cursor()
        try:
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
            con.close()
            return data_dict
        except:
            # rollback DB
            con.rollback()
            return 500
    #USER
    def user_register(self, para =None ):
        # user existed
        try:
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
                    con.close()
                    return 200
                except:
                    # rollback DB
                    con.rollback()
                    return 500
            else:
               return 400
        except:
            # rollback DB
            con.rollback()
            return 500


    def user_login(self, para =None):
        # user existed
        try:
            sql = """select count(*) from taipei_travel_user_info where email = %s and password = %s """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            result = cursor.fetchone()
            # close sql connect
            con.close()
            if result[0] == 1:  # user info match
                return 200
            else:
                return 400
        except:
            # rollback DB
            con.rollback()
            return 500

    def checkLogin(self, para =None):
        #check user login
        try:
            sql = """select * from taipei_travel_user_info where email = %s and password = %s limit 1 """
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            results = cursor.fetchone()

            # close sql connect
            con.close()
            return results
        except:
            # rollback DB
            con.rollback()
            return 500

    #Booking
    def establish_booking(self, para =None):
        try:
            sql = """insert into taipei_travel_booking (email,attractionId,date,time,price)  values (%s,%s,%s,%s,%s)"""
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            con.commit()
            # close sql connect
            con.close()
            return 200
        except:
            # rollback DB
            con.rollback()
            return 500

    def get_booking(self, para =None):
        try:
            sql = """select * from taipei_travel_booking where email = %s order by id DESC limit 1"""
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            result = cursor.fetchone()
            # close sql connect
            con.close()

            if result != None : # not null
                # print(f"para = {para},result={result}")
                email = result[1]
                attractionId = result[2]
                date = result[3]
                time = result[4]
                price = result[5]

                #
                sql = """select name,address from taipei_travel_info where id = %s limit 1"""
                para = (attractionId,)
                con = self.pool.get_connection()
                cursor = con.cursor()
                cursor.execute(sql, para)
                result = cursor.fetchone()
                # close sql connect
                con.close()
                # print(f"para = {para},result={result}")
                name = result[0]
                address = result[1]
                #
                sql = """select link from taipei_travel_images where id = %s limit 1"""
                para = (attractionId,)
                con = self.pool.get_connection()
                cursor = con.cursor()
                cursor.execute(sql, para)
                result = cursor.fetchone()
                # close sql connect
                con.close()
                image = result[0]
                #

                results = []
                results.append(attractionId)
                results.append(name)
                results.append(address)
                results.append(image)
                results.append(date)
                results.append(time)
                results.append(price)
                # print(results)
                return results
            else: #booking = null
                return None
        except:
            # rollback DB
            con.rollback()
            return 500
    def delete_booking(self, para =None):
        try:
            sql = """delete from taipei_travel_booking where email = %s"""
            con = self.pool.get_connection()
            cursor = con.cursor()
            cursor.execute(sql, para)
            print(f"para={para}")
            con.commit()
            # close sql connect
            con.close()
            return 200
        except:
            # rollback DB
            con.rollback()
            return 500

mysql = SQLDB()




