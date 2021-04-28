import mysql.connector
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
        self.conn = mysql.connector.connect(pool_name = "mypool",pool_size = 3,**self.config)
        print("連線成功")

    def Update(self, para= None):
        sql = "REPLACE INTO taipei_travel_info (id, name, category, description, address, transport, mrt, latitude, longitude) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        cursor = self.conn.cursor()
        cursor.execute(sql, para)
        self.conn.commit()

    def save_image_link(self, para = None):
        cursor = self.conn.cursor()
        #link existed or not
        sql = "select count(*) from taipei_travel_images where link = '%s'"
        cursor.execute(sql, para[1])
        result = cursor.fetchone()
        #link not existed
        if result[0] == 0:
            sql = "INSERT INTO taipei_travel_images (id, link) VALUES ('%s', '%s')"
            cursor.execute(sql, para)
            self.conn.commit()
        else:
            return False

    def get_api_attractionId(self, para = None):
        #judge id include invalid character
        try:
            data_dict = {}
            cursor = self.conn.cursor()
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

        cursor = self.conn.cursor()
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

        return data_dict






