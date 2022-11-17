from flask import Flask,render_template,request
app=Flask(__name__)

import ibm_db

conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rsj36993;PWD=9Yvt1EV6cb3DgObg",'','')


@app.route("/")
def home():
    
    # sql= "SELECT * FROM TEST"
    # stmt = ibm_db.exec_immediate(conn, sql)
    # dictionary = ibm_db.fetch_assoc(stmt)
    # while dictionary != False:
    #     print ("The  is : ", dictionary["NAME"])
    #     dictionary = ibm_db.fetch_assoc(stmt)
    return render_template('base.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/regForm',methods = ['POST'])

def regForm():

    if request.method == 'POST':
        try:
            sql= "CREATE TABLE IF NOT EXISTS users (name varchar(256), addr varchar(256), city varchar(256), pin varchar(256), bg varchar(256),email varchar(256), pass varchar(256),usertype varchar(256))"
            stmt = ibm_db.exec_immediate(conn, sql)
            print("table created")
        
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            ty = request.form['bg2']
            email = request.form['em']
            passs = request.form['password']

            values = "('"+name+"','"+addr+"','"+city+"','"+pin+"','"+bg+"','"+email+"','"+passs+"','"+ty+"')"

            sql = "INSERT INTO users (name,addr,city,pin,bg,email,pass,usertype) VALUES "+values
            print(sql)
            stmt = ibm_db.exec_immediate(conn, sql)
            dictionary = ibm_db.fetch_assoc(stmt)
            print(dictionary)
            print("Data added to the table")
        
        except Exception as err:
            print(err)
    return "done"


    

@app.route('/login')
def add():
    return render_template("login.html")





if __name__=='__main__':
    app.run(debug=True)