from triumph import db
from sqlalchemy import PrimaryKeyConstraint


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
    image_urls = db.relationship('ImageUrl', backref=db.backref('product'))

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
    image_urls = db.relationship('ImageUrl', backref=db.backref('sku'))


class ImageUrl(db.Model):
    __tablename__ = 'skuimageurl'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'))




