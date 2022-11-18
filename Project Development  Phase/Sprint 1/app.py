from flask import Flask, render_template, request, redirect, url_for, session,flash
import os
import ibm_db






conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rsj36993;PWD=9Yvt1EV6cb3DgObg",'','')

app = Flask(__name__)



@app.route("/",methods=['GET'])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))
  return render_template('home.html',name='Home')




@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':

    try:
      email = request.form['email']
      username = request.form['username']
      password = request.form['password']
      userType = request.form['type']



    




      

      if not email or not username or not password:
        return render_template('register.html',error='Please fill all fields')
      
      #hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

      query = "SELECT * FROM USERS WHERE Email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      
      print("entering1")
      if not isUser:
        insert_sql = "INSERT INTO Users(Name,email,PASSWORD,usertype) VALUES (?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, username)
        ibm_db.bind_param(prep_stmt, 2, email)
        ibm_db.bind_param(prep_stmt, 3, password)
        ibm_db.bind_param(prep_stmt, 4, userType)
        ibm_db.execute(prep_stmt)
        # print("entering2")


        return render_template('register.html',success="You can login")
      else:
        return render_template('register.html',error='Invalid Credentials')

    except Exception as e:
      print("error",e)

  return render_template('register.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
      return render_template('login.html',error='Please fill all fields')
    query = "SELECT * FROM USERS WHERE Email=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    # print(isUser,password)

    # userType = isUser.USERTYPE
    # print("## ",isUser["USERTYPE"])

    if(isUser and isUser["USERTYPE"]=="Donor"):
      return render_template('Donorhome.html',error='Invalid Credentials')

    if(isUser and isUser["USERTYPE"]=="Recepient"):
      return render_template('Recepienthome.html',error='Invalid Credentials')

    if not isUser:
      return render_template('login.html',error='Invalid Credentials')
      
    #isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

    #if not isPasswordMatch:
    if(isUser['PASSWORD']!=password):
      return render_template('login.html',error='Invalid Credentials')

    session['email'] = isUser['EMAIL']
    return redirect(url_for('home'))

  return render_template('login.html',name='Home')


app.debug = True

if __name__ == "__main__":
  app.run(host="0.0.0.0")
