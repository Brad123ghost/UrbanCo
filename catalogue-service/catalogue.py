from flask import Flask, request, render_template, redirect, make_response, jsonify
import psycopg2
import os
import time

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASS"]
DB = os.environ["DB"]
DB_HOST = os.environ["DB_HOST"]

app = Flask(__name__)

def init_tables():
    CREATE_CATALOGUE_TABLE = "CREATE TABLE IF NOT EXISTS CATALOGUE (\
                        productid serial PRIMARY KEY,\
                        productcode TEXT NOT NULL,\
                        productname TEXT NOT NULL,\
                        productprice MONEY NOT NULL,\
                        productdesc TEXT,\
                        productimage TEXT)"

    CREATE_CATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS CATEGORY (\
                        categoryid serial PRIMARY KEY,\
                        categoryname TEXT NOT NULL)"

    CREATE_PRODUCTCATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS PRODUCTCATEGORY(\
                        productid INTEGER,\
                        categoryid INTEGER,\
                        PRIMARY KEY(productid, categoryid))"

    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_CATALOGUE_TABLE)
    cursor.execute(CREATE_CATEGORY_TABLE)
    cursor.execute(CREATE_PRODUCTCATEGORY_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def insert_data():
    SQL = "INSERT INTO CATALOGUE (productcode, productname, productprice, productdesc, productimage) VALUES (%s, %s, %s, %s, %s)"
    DATA = [
        ('ab-dragon-emb-hoodie-white-front-10005040', 'Dragon Embroidered Box Fit Hoodie', 59.99,'Introducing our Oversize Dragon Hoodie, a fusion of modern streetwear and traditional Japanese aesthetics. This unique hoodie features embroidered dragon illustrations on both arms with Japanese symbols on the front and back. The box fit, slouchy shoulders, and hood offer a relaxed yet laid back look. Style it with a puffer vest to showcase the arm illustrations. Embrace the boldness of the dragon\'s symbolism and make a statement wherever you go. Elevate your streetwear game with this eye-catching hoodie.', '../static/images/products/hoodies/ab-dragon-emb-hoodie-white-front-10005040.webp'),
        ('bd-photosynthesis-hoodie-snow-marle-front-10004945', 'Photosythnesis Graphic Print Hoodie', 59.99, 'Introducing our Photosynthesis Hoodie, crafted from a soft cotton blend for a comfortable composition. Our in-house designed graphics take inspiration from nature, creating a captivating visual experience. Whether you\'re a nature enthusiast or not, these graphics are not to be missed. Elevate your style with this winning hoodie choice that combines comfort, quality, and eye-catching design.', '../static/images/products/hoodies/bd-photosynthesis-hoodie-snow-marle-front-10004945.webp'),
        ('ab-butterfly-emb-box-hooded-sweat-tan-front-10004429', 'Butterfly Embroidered Box Fit Hoodie', 59.99, 'The Butterfly Emb Box Hooded Sweat. We are bringing back our box fit hoodies in style. Supporting a loose-fitting body with slouchy shoulders. Featuring a butterfly embroidery on the front for that extra bit of detail. An easy way to add some style into your daily looks. Woven from cotton blend fabric for a cosy feel.', '../static/images/products/hoodies/ab-butterfly-emb-box-hooded-sweat-tan-front-10004429.webp'),
        ('ab-yoga-retreat-crew-green-front-10004852', 'Yoga Retreat Crew Neck Sweat', 49.99, 'Introducing the Yoga Retreat Crew Neck Sweat, a minimalist design that adds versatility and comfort to your wardrobe. This sweatshirt features drop shoulders and an oversized fit for a relaxed and laid-back style. Made from 100\% cotton, it provides both comfort and durability. Wear it on your daily walks or pair it with jeans or shorts for a casual, effortless look. Experience the perfect blend of quality comfort and style with the Yoga Retreat Crew Neck Sweat.', '../static/images/products/hoodies/ab-yoga-retreat-crew-green-front-10004852.webp'),
        ('ab-ancient-alien-sweat-solid-black-front-10004848', 'Ancient Alien Graphic Print Sweat', 49.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/hoodies/ab-ancient-alien-sweat-solid-black-front-10004848.webp'),
        ('ab-21-skinny-jean-white-front-10001274', 'Absent Skinny Jeans', 59.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-21-skinny-jean-white-front-10001274.webp'),
        ('ab-21-ripped-skinny-jean-baby-blue-front-10001273', 'Ripped Skinny Jeans', 59.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-21-ripped-skinny-jean-baby-blue-front-10001273.webp'),
        ('ab-twill-baggy-cargo-pant-iguana-front-10004572', 'Twill Baggy Cargo Pocket Pants', 69.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-twill-baggy-cargo-pant-iguana-front-10004572.webp'),
        ('ab-baggy-jean-blue-front-10004193', 'Long Rise Baggy Fit Jeans', 59.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-baggy-jean-blue-front-10004193.webp'),
        ('ab-21-taper-jean-solid-black-front-10001268', 'Tapered Fit Jeans', 59.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-21-taper-jean-solid-black-front-10001268.webp'),
        ('ab-dad-fit-jean-swedish-blue-002-front-10003893', 'Dad Fit Relaxed Jeans', 49.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/products/jeans/ab-dad-fit-jean-swedish-blue-002-front-10003893.webp')
    ]
    SQL2 = "INSERT INTO CATEGORY (categoryname) VALUES (%s)"
    DATA2 = (
        ("Hoodies & Sweats",),
        ("Jeans",)
    )
    SQL3 = "INSERT INTO PRODUCTCATEGORY VALUES (%s, %s)"
    DATA3 = [
        (1,1),
        (2,1),
        (3,1),
        (4,1),
        (5,1),
        (6,2),
        (7,2),
        (8,2),
        (9,2),
        (10,2),
        (11,2)
    ]
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)

    cursor = conn.cursor()
    cursor.executemany(SQL, DATA)
    cursor.executemany(SQL2, DATA2)
    cursor.executemany(SQL3, DATA3)
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
        products.append((row[1], row[2], row[3], row[4], row[5]))
    cursor.close()
    conn.close()
    
    return products

@app.route("/catalogue/list", methods=["POST"])
def listcatalogue():
    
    catalogue = load_catalogue()
    
    return {"status_code":200, "list":catalogue}

def get_chosen_category(productcategory):

    categorylist = []

    LOAD_CATEGORY_CATALOGUE = "SELECT * FROM CATALOGUE INNER JOIN PRODUCTCATEGORY ON productcategory.productid=catalogue.productid INNER JOIN CATEGORY ON category.categoryid = productcategory.categoryid WHERE category.categoryname = %s"

    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_CATEGORY_CATALOGUE, [productcategory])
    results = cursor.fetchall()

    for row in results:
        categorylist.append((row[1], row[2], row[3], row[4], row[5]))
    cursor.close()
    conn.close()

    return categorylist

@app.route("/catalogue/category/<productcategory>", methods=["POST"])
def listchosencategory(productcategory):

    chosen_category = get_chosen_category(productcategory)

    return {"status_code":200, "list":chosen_category}
    

# @app.route("/list/<productcategory>", methods=["POST"])
# def latest_chosen_category_products(productcategory):
#     latest = get_chosen_category(productcategory)
#     latest.reverse()

#     del latest[:10]

#     if chosen_category.count() == 0:
#         raise RequestError(404)

#     return {"status_code":200, "list":latest}

def get_product_details(productcode):
    products = []
    # products.append(productcode)
    LOAD_CATALGOUE = "SELECT * FROM CATALOGUE WHERE productcode=%s"
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(LOAD_CATALGOUE, [productcode])
    results = cursor.fetchall()
    # if len(results) == 0:
    #     raise (404)
    for row in results:
        products.append((row[1], row[2], row[3], row[4], row[5]))
    cursor.close()
    conn.close()
    
    return products

@app.route("/catalogue/product/<productcode>", methods=["POST", "GET"])
def displayproduct(productcode):

    product_details = get_product_details(productcode)

    return {"status_code":200, "list":product_details}


time.sleep(12)
init_tables()
insert_data()
app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
# app.run(host="0.0.0.0", port=5000)