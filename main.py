# API REST Using Flask, SQLAlchemy as ORM and Marsmallow
from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask (__name__)

#configuration Database

                                                        #user@password/name_of_db
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root@localhost/sqlalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#create the table of database 
class Products (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))
    image = db.Column(db.String(400))
    
    
    def __init__(self, title, description, image):
        self.title = title
        self.description = description
        self.image = image
        
db.create_all() 

#create the schema of database 
ma = Marshmallow(app)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description','image')


oneProduct = ProductSchema()
manyProducts= ProductSchema(many=True)


#Index
@app.route('/')
def mainPage():
    return {"Message":"This is the main page of my API"}


#Route for add products
@app.route('/add_products', methods=["POST"])
def createProducts():
    
    title = request.json['title']
    description = request.json['description']
    image = request.json['image']
    
    newProduct = Products(title, description,image)
    
    db.session.add(newProduct)
    db.session.commit()
    
    return oneProduct.jsonify(newProduct)  #for see the newProduct added

#Route for GET a specific product
@app.route('/products/<id>', methods=['GET'])   
def getProduct(id):
   #create a variable for received the product
   product = Products.query.get(id)
   
   return oneProduct.jsonify(product)

#route for GET Alls products
@app.route('/products', methods=['GET'])
def allProducts():
    #we perform a query to obtain all the products
    products = Products.query.all()
    result = manyProducts.dump(products)
    
    return manyProducts.jsonify(result)

#route for update a product
@app.route('/update/<id>', methods=['PUT'])
def updateProduct(id):
    #call the product for id
    product = Products.query.get(id)
    
    #We fill in the fields
    title = request.json['title']
    description = request.json['description']
    image = request.json['image']
    
    #we assign the new values
    product.title = title
    product.descriprion = description 
    product.image = image 
    
    #save to database
    db.sessioncommit()
    
    return oneProduct.jsonify(product)

#route for delete a product
@app.route('/delete/<id>', methods= ['DELETE'])
def delProduct(id):
    #call the product for delete
    product = Products.query.get(id)
    
    #GET alls products to show them
    products = Products.query.all()
    alls = manyProducts.dump(products)
    
    #Delete and save in database
    db.session.delete(product)
    db.session.commit()
    
    #return a message and list of products
    return jsonify({"message":"Product deleted"},alls)
    
 





if __name__ == '__main__':
    app.run(debug=True)
    