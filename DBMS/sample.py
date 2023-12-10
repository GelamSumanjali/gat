import sqlite3

conn = sqlite3.connect('GAT.db')
cursor_obj = conn.cursor()
cursor_obj.execute("SELECT regid,password FROM student")
data = cursor_obj.fetchall()
print(type(data))
list_data = []
data_dict = dict()
for i in data:
    list_data.append(list(i))
for i in list_data:
    data_dict[i[0]] = i[1]
    