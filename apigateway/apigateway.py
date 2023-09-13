from flask import Flask, Response, url_for, abort, jsonify
import requests
import os

class Product(object):
    def __init__(self, productcode, productname, productprice, productdesc, productimage):
        self.productcode = productcode
        self.productname = productname
        self.productimage = productimage
        self.productdesc = productdesc
        self.productimage = productimage
        
app = Flask(__name__)

@app.route("/api/list/<productcategory>", methods=["POST", "GET"])
def apicategorycatalogue(productcategory):
    res = requests.post("http://catalogueservice:5000/list/" + str(productcategory))
    categorylist = []
    
    for products in res["list"]:
        categorylist.append(Product(products[0],products[1],products[2],products[3],products[4]))
        
    return res
    # return {"status_code":200, "list":categorylist}

@app.route("/api/catalogue/list", methods=["POST", "GET"])
def apicatalogue():
    
    res = requests.post("http://catalogueservice:5000/catalogue/list").json()
    productslist = []
    
    for products in res["list"]:
        productslist.append(Product(products[0],products[1],products[2],products[3],products[4]))
        
    # return "Hi"
    return {"status_code":200, "list":productslist}

app.run(host="0.0.0.0", port=5000, debug=True)