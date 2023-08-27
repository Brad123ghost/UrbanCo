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
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS CATALOGUE (\
                        productid serial PRIMARY KEY,\
                        productcode TEXT NOT NULL,\
                        productname TEXT NOT NULL,\
                        productprice MONEY NOT NULL,\
                        productdesc TEXT,\
                        productimage TEXT\
                    )"
    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

def insert_data():
    SQL = "INSERT INTO CATALOGUE (productcode, productname, productprice, productdesc, productimage) VALUES (%s, %s, %s, %s, %s)"
    DATA = [
        ('ab-dragon-emb-hoodie-white-front-10005040', 'Dragon Embroidered Box Fit Hoodie', 59.99,'Introducing our Oversize Dragon Hoodie, a fusion of modern streetwear and traditional Japanese aesthetics. This unique hoodie features embroidered dragon illustrations on both arms with Japanese symbols on the front and back. The box fit, slouchy shoulders, and hood offer a relaxed yet laid back look. Style it with a puffer vest to showcase the arm illustrations. Embrace the boldness of the dragon\'s symbolism and make a statement wherever you go. Elevate your streetwear game with this eye-catching hoodie.', '../static/images/ab-dragon-emb-hoodie-white-front-10005040.webp'),
        ('bd-photosynthesis-hoodie-snow-marle-front-10004945', 'Photosythnesis Graphic Print Hoodie', 59.99, 'Introducing our Photosynthesis Hoodie, crafted from a soft cotton blend for a comfortable composition. Our in-house designed graphics take inspiration from nature, creating a captivating visual experience. Whether you\'re a nature enthusiast or not, these graphics are not to be missed. Elevate your style with this winning hoodie choice that combines comfort, quality, and eye-catching design.', '../static/images/bd-photosynthesis-hoodie-snow-marle-front-10004945.webp'),
        ('ab-butterfly-emb-box-hooded-sweat-tan-front-10004429', 'Butterfly Embroidered Box Fit Hoodie', 59.99, 'The Butterfly Emb Box Hooded Sweat. We are bringing back our box fit hoodies in style. Supporting a loose-fitting body with slouchy shoulders. Featuring a butterfly embroidery on the front for that extra bit of detail. An easy way to add some style into your daily looks. Woven from cotton blend fabric for a cosy feel.', '../static/images/ab-butterfly-emb-box-hooded-sweat-tan-front-10004429.webp'),
        ('ab-yoga-retreat-crew-green-front-10004852', 'Yoga Retreat Crew Neck Sweat', 49.99, 'Introducing the Yoga Retreat Crew Neck Sweat, a minimalist design that adds versatility and comfort to your wardrobe. This sweatshirt features drop shoulders and an oversized fit for a relaxed and laid-back style. Made from 100% cotton, it provides both comfort and durability. Wear it on your daily walks or pair it with jeans or shorts for a casual, effortless look. Experience the perfect blend of quality comfort and style with the Yoga Retreat Crew Neck Sweat.', '../static/images/ab-yoga-retreat-crew-green-front-10004852.webp'),
        ('ab-ancient-alien-sweat-solid-black-front-10004848', 'Ancient Alien Graphic Print Sweat', 49.99, 'Introducing the Urban Graphic Sweat - with a crew neck, drop shoulder design, and ribbed neckband, this sweatshirt offers both comfort and a fashionable edge. <br><br>Made for those who appreciate urban fashion and unique details, the Urban Graphic Sweat combines comfort with a touch of luxury. Its metallic gold symbols give it an elevated finish, ensuring you stand out from the crowd.', '../static/images/ab-ancient-alien-sweat-solid-black-front-10004848.webp')
    ]

    conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.executemany(SQL, DATA)
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

time.sleep(12)
init_tables()
insert_data()
app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)