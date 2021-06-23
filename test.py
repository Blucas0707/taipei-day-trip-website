from datetime import datetime

# date1 = datetime(2014,10,21).strftime("%Y-%m-%d")
# print(date1)
# date2 = datetime.now().strftime("%Y-%m-%d")
# print(date2)
#
# print(date2 < date1)


# print(datetime.now().strftime("%Y-%m-%d"))
s = "is2 sentence4 This1 a3"
new_s_list = s.split(" ")
ans = "1234"
for new_s in new_s_list:
    order = new_s[-1]
    word = new_s[:-1]
    print(order,word)
    new_ans = ans.replace(order,word + " ")
    ans = new_ans
print(new_ans)
