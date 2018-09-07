from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from triumph import db
from triumph import login

sku_images = db.Table('sku_images',
                      db.Column('sku_id', db.Integer, db.ForeignKey('sku.id')),
                      db.Column('image_url_id', db.Integer, db.ForeignKey('image_url.id'))
                      )

product_images = db.Table('product_images',
                          db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                          db.Column('image_url_id', db.Integer, db.ForeignKey('image_url.id'))
                          )


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    sub_categories = db.relationship('SubCategory', backref=db.backref('category'))
    products = db.relationship('Product', backref=db.backref('category'))


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    price = db.Column(db.String(16))
    currency = db.Column(db.String(16))
    gender = db.Column(db.String(16))
    description = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))
    skus = db.relationship('Sku', backref=db.backref('product'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('product'), secondary=product_images)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="id"),
    )


class SubCategory(db.Model):
    __tablename__ = 'sub_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    products = db.relationship('Product', backref=db.backref('sub_category'))


class Sku(db.Model):
    __tablename__ = 'sku'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(32))
    size = db.Column(db.String(16))
    price = db.Column(db.String(16))
    currency = db.Column(db.String(16))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('sku'), secondary=sku_images)


class ImageUrl(db.Model):
    __tablename__ = 'image_url'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cartitems = db.relationship('CartItem', backref=db.backref('user'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class CartItem(db.Model):
    __tablename__ = 'cartitem'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    color = db.Column(db.String(32))
    size = db.Column(db.String(16))
    price = db.Column(db.String(16))
    currency = db.Column(db.String(16))
    image_url = db.Column(db.String(1024))
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
