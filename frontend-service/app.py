from flask import Flask, request, render_template, redirect, Response, url_for, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from functools import wraps
import requests
import os

class Product(object):
    def __init__(self, productcode, productname, productprice, productdesc, productimage):
        self.productcode = productcode
        self.productname = productname
        self.productprice = productprice
        self.productimage = productimage
        self.productdesc = productdesc
        self.productimage = productimage

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


class UserFormData(object):
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        
SECRET_KEY = "urbancosecretkey"

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def roles_required(role):
    def decorated_function(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return f(*args, **kwargs)
            else:
                return redirect(url_for("index"))
                
        return wrap
    return decorated_function

@login_manager.user_loader
def load_user(userid):
    res = requests.post("http://accountservice:5000/api/loaduser/" + str(userid)).json()
    
    user = []
    
    for userdata in res["userdata"]:
        user.append((userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[5]))
    
    return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][5])

@app.context_processor
def inject_user():
    return dict(user=current_user)

class RegisterForm(FlaskForm):
    firstname = StringField("firstname", validators=[InputRequired("Please enter your first name")])
    lastname = StringField("lastname", validators=[InputRequired("Please enter your last name")])
    email = StringField("email", validators=[InputRequired("Please enter a valid email")])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    confirmpassword = PasswordField(validators=[InputRequired(), Length(min=4, max=20), EqualTo("passowrd", message="Passwords must match")])

@app.route("/", methods=["POST", "GET"])
def index():     
    hoodieres = requests.post("http://catalogueservice:5000/list/hoodies-sweats").json()
    
    hoodielist = []
    for products in hoodieres["list"]:
        hoodielist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    jeanres = requests.post("http://catalogueservice:5000/list/jeans").json()
    latestjeanslist = []

    for products in jeanres["list"]:
        latestjeanslist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    tshirtres = requests.post("http://catalogueservice:5000/list/tshirts").json()
    tshirtlist = []

    for products in tshirtres["list"]:
        tshirtlist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    # return render_template("index.html")
    return render_template("index.html", hoodies=hoodielist, jeans=latestjeanslist, tshirts=tshirtlist)

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        form_data = {
            "email": email,
            "password": password
        }
         
        res = requests.post("http://accountservice:5000/api/login", data=form_data).json()
        if res["status_code"] == 200:
            res = res["user"]
            user = []
            
            user.append(User(res["userid"], res["firstname"], res["lastname"], res["email"], res["password"], res["role"]))
            
            login_user(user[0])
            return redirect(url_for('index'))
        
        elif res["status_code"] == 418:
            return render_template("login.html", exists=False, logErrMsg="The email or password you have entered is invalid.")
    
    if current_user.is_authenticated:
        return redirect(url_for("account"))
    
    return render_template("login.html", exists=False)

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    return render_template("account.html")

@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=["POST", "GET"])
def register():
    userData = (UserFormData(" ", " ", " "))
    
    if request.method == "POST":
        firstName = request.form["firstname"]
        lastName = request.form["lastname"]
        email = request.form["email"]
        password = request.form["pwd"]
        
        res = requests.post("http://accountservice:5000/api/checkuser/" + str(email)).json()

        form_data = {
            "firstname": firstName,
            "lastname": lastName,
            "email": email,
            "password": password
        }
        
        if res["exists"]:
            userData = (UserFormData(firstName, lastName, email))
            return render_template("login.html", exists=True, user=userData, regErrMsg="Email already exists. Please login or use a different email.", regerr="registrationerror", regsuccess=False)
        else:
            res = requests.post("http://accountservice:5000/api/register", data=form_data)
            return render_template("login.html", exists=False, regsuccess=True)
    
    return render_template("login.html", exists=False, user=userData, errmsg="", regerr="", regsuccess=False)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    return render_template("payment.html")

@app.route("/catalogue", methods=["GET"])
def catalogue():
    res = requests.post("http://apigateway:5000/catalogue/list").json()

    productslist = res["list"]
    
    for products in res["list"]:
        productslist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    # return res
    return render_template("catalogue.html", products=productslist)

@app.route("/product", methods=["GET"])
def product():
    return render_template("product.html")

@app.route("/<productcategory>", methods=["GET", "POST"])
def cateloguecategory(productcategory):
    res = requests.post("http://catalogueservice:5000/catalogue/category/" + str(productcategory)).json()
    # res = requests.post("http://apigateway:5000/api/list/" + str(productcategory)).json()
    categorylist = []

    if len(res["list"]) == 0:
        abort(404)

    for product in res["list"]:
        categorylist.append(Product(product[0],product[1],product[2],product[3],product[4]))

    productcategory = productcategory.capitalize()

    if productcategory == "Hoodies-sweats":
        productcategory = "Hoodies & Sweats"
    elif productcategory == "Tshirts":
        productcategory = "T-Shirts"
     
    return render_template("category.html", products=categorylist, category=productcategory)

# Admin Pages
@app.route("/dashboard", methods=["GET"])
@roles_required("Admin")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    return render_template("inventory.html")

@app.route("/product/<productcode>", methods=["GET", "POST"])
def view_product(productcode):
    res = requests.post("http://catalogueservice:5000/catalogue/product/" + str(productcode)).json()

    if len(res["list"]) == 0:
        abort(404)

    product_details = []
 
    for product in res["list"]:
        product_details.append(Product(product[0],product[1],product[2],product[3],product[4]))

    return render_template("product.html", product_details=product_details)


@app.route("/inventory/addnewproduct", methods=["POST"])
def addnewproduct():
    return render_template("addnewproduct.html")

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('error.html', error="403 Forbidden")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html', error="404 Not Found")


app.run(host="0.0.0.0", port=5000, debug=True)
# app.run(host="0.0.0.0", port=5000)