from flask import *  
import sqlite3
import random
import mail
from datetime import datetime, timedelta, date

app=Flask(__name__,template_folder='templates',static_folder='static') 
 
@app.route('/')  

def message():  
    return render_template("index.html")  

@app.route('/register', methods=['POST','GET'])
def register():
    return render_template("register.html")


@app.route('/payment', methods = ['POST', 'GET'])
def payment():
    global aname,fname,cnumber,email,aadhar,password,dte,center
    if request.method == "POST":
        aname = request.form["aname"]  
        fname = request.form["fname"]  
        cnumber = request.form["cnumber"] 
        email = request.form['email']
        aadhar = request.form['aadhar']
        password = request.form['password']
        center = request.form['center']
        with sqlite3.connect("GAT.db") as con:  
                con.execute('''CREATE TABLE IF NOT EXISTS student (
                    regid varchar(4),
                    aname varchar(20),
                    fname varchar(20),
                    cnumber varchar(10),
                    email varchar(30),
                    aadhar varchar(13),
                    password varchar(20))''')
                con.execute("""CREATE TABLE IF NOT EXISTS exam (
                    regid varchar(4),
                    date varchar(10),
                    time varchar(5),
                    center varchar(20))""")
                con.commit()    
        con = sqlite3.connect("GAT.db")
        con.execute("SELECT regid,password FROM student")
        cursor_obj = con.cursor()
        cursor_obj.execute("SELECT regid,password FROM student")
        data = cursor_obj.fetchall()
        if len(data)==0:
            dte = date.today()
        else:
            x = data[-1][-1]
            dte = (datetime.strptime(x, '%d-%m-%Y') + timedelta(days=1)).strftime('%d-%m-%Y')
    return render_template("payment.html")

@app.route('/success')
def success():
    global regid,time
    #print(type(name))
    regid = random.randint(1000,9999)
    mail.email(email,regid,password)
    list1 = ['9','1']
    time = random.choice(list1)
    if time=='9':
        time = '9:00am'
    else:
        time = '1:00pm'
    with sqlite3.connect("GAT.db") as con:
        con.execute(
        "INSERT into student (regid, aname, fname, cnumber, email, aadhar, password,date,time,center) values (?,?,?,?,?,?,?,?,?,?)",(regid, aname, fname, cnumber, email, aadhar, password,dte,time,center))
    return render_template("success.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")
@app.route('/home', methods = ['POST'])
def home():
    regid = request.form['regid']
    password = request.form['password']
    con = sqlite3.connect("GAT.db")
    #con.execute("SELECT regid,password FROM student")
    cursor_obj = con.cursor()
    cursor_obj.execute("SELECT regid,password FROM student")
    data = cursor_obj.fetchall()
    list_data = []
    data_dict = dict()
    for i in data:
        list_data.append(list(i))
    for i in list_data:
        data_dict[i[0]] = i[1]
    for i in list_data:
        if regid in i:
            if data_dict[regid] != password:
                return  "Wrong password or Registration id"
            else:
                cursor_obj = con.cursor()
                cursor_obj.execute("SELECT  regid,aname,email,date,time,center FROM student")
                data = cursor_obj.fetchall()
                for i in data:
                    if regid in i:
                        regid = i[0]
                        aname = i[1]
                        email = i[2]
                        date = i[3]
                        time = i[4]
                        center = i[5]
                return render_template("home.html",aname = aname,regid = regid, email = email, date = date, time = time, center = center )
        else:
            return "Invalid Registration Id"
        
if __name__ == '__main__':  
   app.run(debug = True)  