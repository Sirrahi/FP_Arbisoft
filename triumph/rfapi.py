from flask_restful import Resource
from triumph import api
from flask import jsonify, abort
from triumph.models import Category, Item, Sku


class Categories(Resource):
    def get(self):
        raw_categories = Category.query.all()
        categories = []
        for category in raw_categories:
            categories.append({'name': category.name, 'id': category.id})

        return jsonify({'categories': categories})


class Products(Resource):
    def get(self, category_id):
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            abort(404)
        products = []
        for product in category.items:
            products.append({'name': product.name, 'id': product.id})

        return jsonify({'products': products})


class Product(Resource):
    def get(self, product_id):
        item = Item.query.filter_by(id=product_id).first()
        features = []

        for feature in item.features:
            features.append(feature.name)

        image_urls = []

        for image_url in item.image_urls:
            image_urls.append(image_url.url)

        return jsonify({'id': item.id, 'name': item.name, 'brand': item.brand,
                        'description': item.description, 'features': features, 'image_urls': image_urls})


class Skus(Resource):
    def get(self, product_id):
        item = Item.query.filter_by(id=product_id).first()
        skus = []

        for sku in item.skus:
            skus.append({'id': sku.id, 'color': sku.color})

        return jsonify({'skus': skus})


class SpecificSku(Resource):
    def get(self, sku_id):
        sku = Sku.query.filter_by(id=sku_id).first()
        image_urls = []

        for image_url in sku.image_urls:
            image_urls.append(image_url.url)

        return jsonify({'id': sku.id, 'color': sku.color, 'size': sku.size, 'price': sku.price,
                        'currency': sku.currency, 'image_urls': image_urls})


api.add_resource(Categories, '/categories', endpoint='categories')
api.add_resource(Products, '/categories/<int:category_id>/products', endpoint='products')
api.add_resource(Product, '/products/<int:product_id>', endpoint='product')
api.add_resource(Skus, '/products/<int:product_id>/skus', endpoint='skus')
api.add_resource(SpecificSku, '/skus/<int:sku_id>', endpoint='sku')
