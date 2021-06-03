from datetime import datetime
date1 = datetime(2014,10,21).strftime("%Y-%m-%d")
print(date1)
date2 = datetime.now().strftime("%Y-%m-%d")
print(date2)

print(date2 < date1)
# print(datetime.now().strftime("%Y%m%d%H%M%S"))