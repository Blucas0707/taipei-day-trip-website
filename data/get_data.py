import json
from SQL import SQLDB

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
    mysql.Update(para)

    # save image links to sql table - taipei_travel_images
    # only return .jpg or .png image links
    images = get_image_link(detail["file"])
    for link in images:
        para = (id,link)
        # print(para)
        mysql.save_image_link(para)



