from flask import Flask, render_template, url_for, redirect, session, request, jsonify, json
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from functools import wraps
import psycopg2
import os
import time
import requests
# import json

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASS"]
DB = os.environ["DB"]
DB_HOST = os.environ["DB_HOST"]
SECRET_KEY = "urbancosecretkey"


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def roles_required(role):
    def decorated_function(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role == role:
                return f(*args, **kwargs)
            else:
                return redirect(url_for("login"))
                
        return wrap
    return decorated_function

class User(UserMixin):
    def __init__(self, userid, firstname, lastname, email, password, role, active=True):
        self.userid = userid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role
        self.active = active
    
    def get_id(self):
        return self.userid
    
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active
    
    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

def to_json(obj):
    if isinstance(obj, User):
        return {
            "firstname": obj.firstname,
            "lastname": obj.lastname,
            "email": obj.email,
            "password": obj.password,
            "role": obj.role
        }

@login_manager.user_loader
def load_user(userid):
    LOAD_USER = "SELECT * FROM USERS INNER JOIN USERGROUPS ON usergroups.userid=users.userid INNER JOIN GROUPS ON groups.groupid=usergroups.groupid WHERE users.userid = %s"
    USERID = [userid]
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_USER, USERID)
    results = cursor.fetchall()
    
    # user = []
    # for userdata in results:
    #     user.append(User(userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[8]))
    
    cursor.close()
    conn.close()
    # print(user)
    return User(results[0][0], results[0][1], results[0][2], results[0][3], results[0][4], results[0][8])
    
class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired()], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[InputRequired()], render_kw={"placeholder": "Last Name"})
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Register")
    
    def validate_username(self, email):
        CHECK_EXISTING_USER = "SELECT * FROM USER WHERE email=%s"
        
        conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(CHECK_EXISTING_USER, email)
        results = cursor.fetchall()
        
        if len(results) != 0:
            raise ValidationError("That email is already registered. Please Login instead.")
        
        cursor.close()
        conn.close()


class loginForm(FlaskForm):
    email = StringField(validators=[InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")
    
    
def init_tables():
    CREATE_USER_TABLE = "CREATE TABLE IF NOT EXISTS USERS (\
        userid serial PRIMARY KEY,\
        firstname VARCHAR(50) NOT NULL,\
        lastname VARCHAR(50) NOT NULL,\
        email VARCHAR(80) NOT NULL UNIQUE,\
        password TEXT NOT NULL)"
        
    CREATE_ROLE_TABLE = "CREATE TABLE IF NOT EXISTS GROUPS(\
        groupid serial PRIMARY KEY,\
        groupname TEXT NOT NULL)"
        
    CREATE_USERROLE_TABLE = "CREATE TABLE IF NOT EXISTS USERGROUPS(\
        userid INTEGER,\
        groupid INTEGER,\
        PRIMARY KEY(userid, groupid))"
        
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_USER_TABLE)
    cursor.execute(CREATE_ROLE_TABLE)
    cursor.execute(CREATE_USERROLE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()
    
def insert_data():
    SQL = "INSERT INTO USERS (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
    DATA = [
        ('UrbanCo', 'Admin', 'admin@urbanco.com', '$2b$12$C.t2TorWKegIURaHOS4vceDVCO4gdPCh.AvQhRcXrMYRNlPU6yUlm'),
        ('John', 'Smith', 'customer1@gmail.com','$2b$12$dsyaPsttQpTNJo.SUCTlDe.NLJRvggN4Wi1mZyu7RrKYWL7bTqnXW')
    ]
    
    SQL2 = "INSERT INTO GROUPS (groupname) VALUES (%s)"
    DATA2 = [
        ('Admin',),
        ('Customer',)
    ]
    
    SQL3 = "INSERT INTO USERGROUPS VALUES (%s, %s)"
    DATA3 = [
        (1, 1),
        (2, 2)
    ]
    
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    
    cursor = conn.cursor()
    cursor.executemany(SQL, DATA)
    cursor.executemany(SQL2, DATA2)
    cursor.executemany(SQL3, DATA3)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/api/checkuser/<email>", methods=["POST", "GET"])
def check_user(email):
    CHECK_EXISTING_USER = "SELECT * FROM USERS WHERE email=%s"
    
    EMAIL = [
        (email,)
    ]
    
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CHECK_EXISTING_USER, EMAIL)
    results = cursor.fetchall()
    
    inDB = False
    
    if len(results) != 0:
        # raise ValidationError("That email is already registered. Please Login instead.")
        inDB = True
        
    cursor.close()
    conn.close()
    
    return {"status_code": 200, "exists":inDB}

@app.route("/api/loaduser/<userid>", methods=["POST", "GET"])
def getUser(userid):
    LOAD_USER = "SELECT * FROM USERS INNER JOIN USERGROUPS ON usergroups.userid=users.userid INNER JOIN GROUPS ON groups.groupid=usergroups.groupid WHERE users.userid = %s"
    USERID = [
        (userid,)
    ]
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_USER, USERID)
    results = cursor.fetchall()
    
    userdata = []
    for user in results:
        userdata.append((user[0], user[1], user[2], user[3], user[4], user[8]))
    
    cursor.close()
    conn.close()
    # print(user)
    return {"status_code": 200, "userdata":userdata}

@app.route("/api/getuser/<userid>", methods=["POST", "GET"])
def is_admin(userid):
    USER_WITH_ROLE_SQL = "SELECT groupname FROM USERS INNER JOIN USERGROUPS ON usergroups.userid=users.userid INNER JOIN GROUPS ON groups.groupid=usergroups.groupid WHERE users.userid = %s"
    USERID = [
        (userid,)
    ]
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(USER_WITH_ROLE_SQL, USERID)
    results = cursor.fetchall()
    
    authorized = (results[0][0] == "Admin")
    
    if authorized:
        return "Admin, Authorized"
    
    return "Customer, Unauthorized"
    

@app.route("/", methods=["POST", "GET"])
def index():
    user = current_user
    return render_template("index.html", user=current_user)    

@app.route("/account/api/login", methods=["POST", "GET"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    test = [
        (email),
        (password)
    ]
    
    # return {"status_code":200, "list":test}
    # form = loginForm()
    
    # # if form.validate_on_submit():
    SEARCH_USER = "SELECT * FROM USERS INNER JOIN USERGROUPS ON usergroups.userid=users.userid INNER JOIN GROUPS ON groups.groupid=usergroups.groupid WHERE email = %s"
    DATA = [
        (email)
    ]
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(SEARCH_USER, DATA)
    results = cursor.fetchall()
    userlist = []
    for row in results:
        # userlist.append((row[0], row[1], row[2], row[3], row[4], row[8]))
        userlist.append(User(row[0], row[1], row[2], row[3], row[4], row[8]))
        
    user = []
    if len(userlist) != 0:
        if bcrypt.check_password_hash(userlist[0].password, password):
            # login_user(userlist[0])

            # return current_user.role
            return {"status_code":200, "user":json.loads(json.dumps(userlist[0].__dict__))}
            # return redirect(url_for('index'))
    
    cursor.close()
    conn.close()

    # return {"status_code":200, "user":"Success"}
    return render_template("login.html", form=form)

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
@roles_required("Admin")
def dashboard():
    return ("Welcome to the Admin dashboard " + str(current_user.firstname) + ". You have " + str(current_user.role) + " access!")
    # return render_template("dashboard.html")

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    return render_template("account.html", user=current_user)

@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        INSERT_NEW_USER = "INSERT INTO USERS (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)"
        USER_DATA = [(form.firstname.data, form.lastname.data, form.email.data, hashed_password)]
        
        conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)

        cursor = conn.cursor()
        cursor.executemany(INSERT_NEW_USER, USER_DATA)
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for("login"))   
        
    return render_template("register.html", form=form)

time.sleep(15)
init_tables()
insert_data()

app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)