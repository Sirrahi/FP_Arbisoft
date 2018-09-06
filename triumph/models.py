from triumph import db
from sqlalchemy import PrimaryKeyConstraint

product_category = db.Table('product_category', db.metadata,
                         db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                         db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                         )


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    features = db.relationship('Feature', backref=db.backref('category'))
    products = db.relationship('Product', backref=db.backref('category', lazy='dynamic'), secondary=product_category)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    gender = db.Column(db.String(16))
    description = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'))
    skus = db.relationship('Sku', backref=db.backref('sku_product'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('image_product'))

    __table_args__ = (
        PrimaryKeyConstraint("id", name="id"),
    )


class Feature(db.Model):
    __tablename__ = 'feature'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    products = db.relationship('Product', backref=db.backref('feature'))


class Sku(db.Model):
    __tablename__ = 'sku'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(32))
    size = db.Column(db.String(16))
    price = db.Column(db.String(16))
    currency = db.Column(db.String(16))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image_urls = db.relationship('ImageUrl', backref=db.backref('image_sku'))


class ImageUrl(db.Model):
    __tablename__ = 'skuimageurl'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    sku_id = db.Column(db.Integer, db.ForeignKey('sku.id'))




