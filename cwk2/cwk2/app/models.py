from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


user_product = db.Table('user_product', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('Product.pid'))
)

class User(UserMixin,db.Model):
    __tablename__= 'User'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(500), index=True)  
    password = db.Column(db.String(32), index=True)
    email = db.Column(db.String(500), index=True)
    products = db.relationship("Product",secondary = "user_product",backref = "users")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def is_active(self):
        return True


    def __init__(self,user,password,email):
        self.user = user
        self.password= password
        self.email = email




class Product(db.Model):
    __tablename__ = "Product"
    pid = db.Column(db.Integer,primary_key = True)
    itemname = db.Column(db.String(500),index = True)
    itemcost = db.Column(db.Integer,index = True)
    itemdesc = db.Column(db.String(500),index = True)
    itemurl = db.Column(db.String(1000),index = True)
    # likes = db.Column(db.Integer,index = True,default = 0)
    # status = db.Column(db.String(50),index = True,default = "UNLIKED")
    
    def __init__(self,itemname,itemcost):
        self.itemname = itemname
        self.itemcost = itemcost
        self.itemdesc = itemdesc
        self.itemurl  = itemurl





