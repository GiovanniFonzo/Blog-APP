'''
-- CA A Basic Blogging App
-- Name: Giovanni Fonzo
-- Student ID: D19124775
-- Module: Programming and Algorithms 2 CMPU1017: 2020-21
-- Year: 2020/2021 
-- Course: DT249 - Stage 2
-- D19124775_GiovanniFonzo_BasicBloggingApp
'''

from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


@app.route('/login')
def hello():
    uname = request.args.get('uname')
    pass_ = request.args.get('pass')
    #print(uname + ', ' + pass_)
    c = create_connection("database.db").cursor()
    c.execute("select * from User")
    rows = c.fetchall()
    for row in rows:
        id = str(row[1])
        pas = str(row[5])
        if id == uname:
            if pas == pass_:
                return "Correct"
            else:
                return "Incorrect Pass"
    return "Incorrect ID"


@app.route('/post_blog', methods=["post", "get"])
def post():
    print(request.args.get('data'))
    return "Posted..."

'''
@app.route('/post_blog', methods=["post", "get"])
def post():
    print(request.args.get('data'))
    return "Posted..."'''

@app.route('/register')
def register():
    #data = "?fname=" + f + "&lname=" + l + "&email=" + email + "&token=" + str(token) + "&pass=" + p + 
    # "&is_admin=" + is_admin + "&created=" + created + "&modified=" + modified 

    #id = "1234"
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    email = request.args.get('email')
    token = request.args.get('token')
    passw = request.args.get('pass')
    is_admin = request.args.get('is_admin')
    created = request.args.get('created')
    modified = request.args.get('modified')
    
    conn = create_connection('database.db')
    try:
        c = conn.cursor()
        print("cursor created")
    except:
        print('No connection')

    c.execute('select * from User')
    a = c.fetchone()
    try:
        id = str(int(a[0]) + 1)
    except:
        print(a)
        id = 0



    query = "INSERT INTO User(id,first_name,last_name,email,token,password, is_admin,created,updated)"
    query = query + "VALUES(" + "\"" + str(id) + "\"" + ',' + "\"" + fname + "\"" + ',' + "\"" + lname + "\"" + ',' + "\"" + email + "\"" + ',' + "\"" + token + "\"" + ',' + "\"" + passw + "\"" + ',' + "\"" + is_admin + "\"" + ',' + "\"" + created + "\"" + ',' + "\"" + modified + "\")"
    print(query)
    #data = (id, fname, lname, email, token, passw, is_admin, created, modified)
    
    try:
        c.execute(query)
        conn.commit()
        print("Registered")
    except sqlite3.Error as er:
        print("Couldn't register")
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    return "Reg"



if __name__ == '__main__':
    app.run()