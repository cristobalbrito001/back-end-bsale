from flask import Flask,jsonify
from config import config
from flask_mysqldb import MySQL
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})

conexion = MySQL(app)
@app.route('/')
def index():
    return "index!"

@app.route('/product', methods=['GET'])
def list_product():
    try:
       cursor = conexion.connection.cursor()
       sql= "SELECT id,name, url_image, price, discount,category FROM product"
       cursor.execute(sql)
       data= cursor.fetchall()
       products = []
       for fila in data:
           product = {'id':fila[0],'name':fila[1], 'url_image':fila[2], 'price':fila[3], 'discount':fila[4],'category':fila[5]}
           products.append(product)
       return jsonify({'products':products, 'mensaje':'productos'})
    except Exception as ex:
        return jsonify({'mensaje':'error'})

@app.route('/categorias/<categoria>', methods=['GET'])
def categorias_search(categoria):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT p.name, p.url_image, p.price, p.discount,p.category FROM product AS p JOIN category AS c ON (p.category = c.id) where c.name='{0}'".format(categoria)
        cursor.execute(sql)
        datos = cursor.fetchall()
        categories = []
        for fila in datos:
            categorie = {'name':fila[0], 'url_image':fila[1], 'price':fila[2], 'discount':fila[3],'category':fila[4]}
            categories.append(categorie)
        return jsonify({'categoria':categories, 'mensaje':'exito'})
    except Exception as ex:
        return jsonify({'mensaje':'error'})

@app.route('/nombre/<nombre>', methods=['GET'])

def name_search(nombre):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT name, url_image, price, discount,category FROM product where name LIKE '%{0}%'".format(nombre.lower())
        cursor.execute(sql)
        datos = cursor.fetchall()
        products = []
        for fila in datos:
            product = {'name': fila[0], 'url_image': fila[1], 'price': fila[2], 'discount': fila[3], 'category':fila[4]}
            products.append(product)
        return jsonify({'products': products, 'mensaje':'exito'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route('/categoria', methods=['GET'])

def list_category():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT name FROM category"
        cursor.execute(sql)
        datos = cursor.fetchall()
        names = []
        for fila in datos:
            nomrbe = {'name': fila}
            names.append(nomrbe)
        return jsonify({'names': names})
    except Exception as ex:
        return jsonify({'mensaje':'error'})
        
@app.route('/product/<id>', methods=['GET'])

def unique_product(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT  name, url_image, price, discount,category  FROM product WHERE id = {0}".format(id)
        cursor.execute(sql)
        datos = cursor.fetchall()
        product_unique = []
        for fila in datos:
            product = {'name': fila[0], 'url_image': fila[1], 'price': fila[2], 'discount': fila[3], 'category':fila[4]}
            product_unique.append(product)
        return jsonify({'products': product_unique})
    except Exception as ex:
        return jsonify({'mensaje':ex}) 

def page_not_found(error):
    return "<h1>pagina no encontrada</h1>"

if __name__ == '__main__':
    app.config.from_object(config['develoment'])
    app.register_error_handler(404,page_not_found )
    app.run()