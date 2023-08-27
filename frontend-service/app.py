from flask import Flask, request, render_template, redirect, Response
import requests
import os

class Product(object):
    def __init__(self, productid, productcode, productname, productprice, productdesc, productimage):
        self.productid = productid
        self.productcode = productcode
        self.productname = productname
        self.productprice = productprice
        self.productdesc = productdesc
        self.productimage = productimage

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    # if request.method == "POST":
    #     name = request.form["name"]
    #     categories = request.form["categories"]
        
    #     res = requests.post("http://gatewayservice:5000/categories")
        
    #     if res.status_code == 200:
    #         return redirect("/categories")
    
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/catalogue", methods=["GET"])
def catalogue():
    
    res = requests.post("http://backend:5000/catalogue/list").json()
    catalogue = []
    
    for category in res["list"]:
        catalogue.append(Product(category[0],category[1],category[2]))
    
    return render_template("catalogue.html", catalogue=catalogue)

@app.route("/product", methods=["GET"])
def product():
    return render_template("product.html")



app.run(host="0.0.0.0", port=5000, debug=True)