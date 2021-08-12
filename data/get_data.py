import json
from mysql.connector import pooling
from dotenv import dotenv_values
import json
#load .env config
config = dotenv_values("../../key/.env")
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
        self.pool = pooling.MySQLConnectionPool(pool_name = "SQLpool",pool_size = 4,pool_reset_session=True,**self.config)
        self.conn = self.pool.get_connection()
        print("Connection Pool Name - ", self.pool.pool_name)
        print("Connection Pool Size - ", self.pool.pool_size)
        print("POOL連線成功-travel")

    def save_image_link(self, para = None):
        cursor = self.conn.cursor()
        #link existed or not
        sql = "select count(*) from taipei_travel_images where link = '%s'"
        cursor.execute(sql, para[1])
        result = cursor.fetchone()
        #link not existed
        if result[0] == 0:
            sql = "INSERT INTO taipei_travel_images (attractionid, link) VALUES (%s, %s)"
            cursor.execute(sql, para)
            self.conn.commit()
        else:
            return False

#Read json file
with open("taipei-attractions.json") as f:
    file_content = json.load(f)
#Rewrite json with better indent = 4
with open("new_data.json","w") as f_write:
    json.dump(file_content,f_write, ensure_ascii= False, indent= 4)

#connect to sql
mysql = SQLDB()

#only return .jpg or .png image links
def get_image_link(image_links):
    image_link_list = image_links.split("http://")
    image_links = []
    for link in image_link_list:
        if link[-3:].lower() == 'jpg' or link[-3:].lower() == 'png':
            image_links.append("http://" + link)
    return tuple(image_links)

#get data from json
travel_details = file_content["result"]["results"]

#get travel info and save to sql-table : taipei_travel_info
for detail in travel_details:
    id = detail["_id"]
    name = detail["stitle"]
    category = detail["CAT2"]
    description = detail["xbody"]
    address = detail["address"]
    transport = detail["info"]
    mrt = detail["MRT"]
    latitude = detail["latitude"]
    longitude = detail["longitude"]

    # #save to sql table- taipei_travel_info
    para = [id, name, category, description, address, transport, mrt, latitude, longitude]
    for i in range(len(para)):
        if para[i] == None:
            para[i] = -1
    para = tuple(para)
    # mysql.Update(para)

    # save image links to sql table - taipei_travel_images
    # only return .jpg or .png image links
    images = get_image_link(detail["file"])
    for link in images:
        para = (id,link)
        print(para)
        mysql.save_image_link(para)



