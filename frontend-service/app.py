from flask import Flask, request, render_template, redirect, Response, url_for
import requests
import os

class Product(object):
    # def __init__(self, productcode, productname, productprice, productdesc, productimage):
    #     self.productcode = productcode
    #     self.productname = productname
    #     self.productprice = productprice
    #     self.productdesc = productdesc
    #     self.productimage = productimage

    def __init__(self, productcode, productname, productprice, productdesc, productimage):
        self.productcode = productcode
        self.productname = productname
        self.productimage = productimage
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
        productslist.append(Product(products[0],products[1],products[2],products[3],products[4]))
    
    return render_template("catalogue.html", products=productslist)

@app.route("/product", methods=["GET"])
def product():
    return render_template("product.html")

@app.route("/jeans", methods=["GET"])
def jeans():
    jeanslist 
    return render_template("jeans.html" products=jeanslist)

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

@app.route("/product/<productcode>", methods=["GET", "POST"])
def view_product(productcode):
    # res = requests.post("http://catalogueservice:5000/catalogue/list").json()
    res = requests.post("http://catalogueservice:5000/catalogue/product/"+str(productcode)).json()
    # res = url_for("http://catalogueservice/displayproduct", productcode=productcode).json()
    product_details = []

    for product in res["list"]:
        product_details.append(Product(product[0],product[1],product[2],product[3],product[4]))

    return render_template("product.html", product_details=product_details)

@app.route("/inventory/addnewproduct", methods=["POST"])
def addnewproduct():
    return render_template("addnewproduct.html")
app.run(host="0.0.0.0", port=5000, debug=True)
# app.run(host="0.0.0.0", port=5000)