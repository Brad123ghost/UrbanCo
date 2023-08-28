from flask import Flask, request, render_template, redirect, Response
import requests
import os

class Product(object):
    def __init__(self, productcode, productname, productprice, productdesc, productimage):
        self.productcode = productcode
        self.productname = productname
        self.productprice = productprice
        self.productdesc = productdesc
        self.productimage = productimage

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        categories = request.form["catalogue"]
        
        res = requests.post("http://local:5000/catalogue")
        
        if res.status_code == 200:
            return redirect("/catalogue")
    
    return render_template("index.html")

@app.route("/catalogue", methods=["GET"])
def catalogue():
    
    res = requests.post("http://catalogueservice:5000/catalogue/list").json()
    productslist = []
    
    for products in res["list"]:
        productslist.append(Product(products[1],products[2],products[3],products[4],products[5]))
    
    return render_template("catalogue.html", products=productslist)

@app.route("/product", methods=["GET"])
def product():
    return render_template("product.html")

@app.route("/jeans", methods=["GET"])
def jeans():
    return render_template("jeans.html")

@app.route("/hoodies-sweats", methods=["GET"])
def hoodie_sweats():
    return render_template("hoodies-sweats.html")

# Admin Pages
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    return render_template("inventory.html")
app.run(host="0.0.0.0", port=5000, debug=True)