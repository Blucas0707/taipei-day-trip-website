from Model.SQL import *

class Order(SQLDB):
    def establish_order(self, para =None):
        try:
            sql = """insert into taipei_travel_orders (prime,price,attraction_id,
                    attraction_name,attraction_address,attraction_image,date,time,name,email,phone,order_id)  
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