from flask import Flask, request, render_template, redirect, Response, url_for, abort
from flask_login import UserMixin
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

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():     
    # hoodieres = requests.post("http://catalogueservice:5000/list/hoodies-sweats").json()
    
    # hoodielist = []
    # for products in hoodieres["list"]:
    #     hoodielist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    # jeanres = requests.post("http://catalogueservice:5000/list/jeans").json()
    # latestjeanslist = []

    # for products in jeanres["list"]:
    #     latestjeanslist.append(Product(products[0],products[1],products[2],products[3],products[4]))

    return render_template("index.html")
    # return render_template("index.html", hoodies=hoodielist, jeans=latestjeanslist)

@app.route("/login", methods=["POST", "GET"])
def login():
    # return redirect("http://accountservice:5000/login", code=200)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        form_data = {
            "email": email,
            "password": password
        }
        
        res = requests.post("http://accountservice:5000/account/api/login", data=form_data).json()
        
        return res["list"]
    
    return render_template("login.html")

# @app.route("/account/login", methods=["POST"])
# def account_login(email, password):
#     res = 

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        firstName = request.form["firstname"]
        lastName = request.form["lastname"]
        email = request.form["email"]
        password = request.form["pwd"]
        
        return firstName
    
    return render_template("login.html")

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

    if productcategory == "hoodies-sweats":
        productcategory = "Hoodies & Sweats"
        
    return render_template("category.html", products=categorylist, category=productcategory)

# Admin Pages
@app.route("/dashboard", methods=["GET"])
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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html'), 404
app.run(host="0.0.0.0", port=5000, debug=True)
# app.run(host="0.0.0.0", port=5000)