from flask import Flask, request, render_template, redirect
import psycopg2
import os
import time

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASS"]
DB = os.environ["DB"]
DB_HOST = os.environ["DB_HOST"]

app = Flask(__name__)

def init_tables():
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS CATALOGUE (productid serial PRIMARY KEY, productcode TEXT NOT NULL, productname TEXT NOT NULL, productprice INT NOT NULL, productdesc TEXT, productimage TEXT)"
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def load_catalogue():
    
    products = []
    
    LOAD_CATALGOUE = "SELECT * FROM CATALOGUE"
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_CATALGOUE)
    results = cursor.fetchall()

    for row in results:
        products.append((row[0], row[1], row[2], row[3], row[4], row[5]))
    cursor.close()
    conn.close()

    return products

@app.route("/catalogue/list", methods=["POST"])
def listcatalogue():
    
    catalogue = load_catalogue()
    
    return {"success":True, "list":catalogue}

time.sleep(20)
init_tables()
app.run(host="0.0.0.0", port=5000, debug=True)