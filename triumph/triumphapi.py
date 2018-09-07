from flask import jsonify, abort
from flask_restful import Resource

from triumph import api
from triumph.models import Category, Product, Sku, SubCategory


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

        for product in category.products:
            products.append({'name': product.name, 'id': product.id})

        return jsonify({'products': products})


class SubCategories(Resource):
    def get(self, category_id):
        category = Category.query.filter_by(id=category_id).first()

        if category is None:
            abort(404)

        sub_categories = []

        for sub_category in category.sub_categories:
            sub_categories.append({'name': sub_category.name, 'id': sub_category.id})

        return jsonify({'sub_categories': sub_categories})


class _Product(Resource):
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first()

        if product is None:
            abort(404)

        image_urls = []

        for image_url in product.image_urls:
            image_urls.append(image_url.url)

        return jsonify({'id': product.id, 'name': product.name, 'brand': product.brand,
                        'price': product.price, 'currency': product.currency, 'gender': product.gender,
                        'description': product.description, 'image_urls': image_urls})


class _SubCategory(Resource):
    def get(self, sub_category_id):
        sub_category = SubCategory.query.filter_by(id=sub_category_id).first()

        if sub_category is None:
            abort(404)

        products = []

        for product in sub_category.products:
            products.append({'name': product.name, 'id': product.id})

        return jsonify({'products': products})


class Skus(Resource):
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first()

        if product is None:
            abort(404)

        skus = []

        for sku in product.skus:
            skus.append({'id': sku.id, 'color': sku.color})

        return jsonify({'skus': skus})


class SpecificSku(Resource):
    def get(self, sku_id):
        sku = Sku.query.filter_by(id=sku_id).first()

        if sku is None:
            abort(404)

        image_urls = []

        for image_url in sku.image_urls:
            image_urls.append(image_url.url)

        return jsonify({'id': sku.id, 'color': sku.color, 'size': sku.size, 'price': sku.price,
                        'currency': sku.currency, 'image_urls': image_urls})


api.add_resource(Categories, '/categories', endpoint='categories')
api.add_resource(Products, '/categories/<int:category_id>/products', endpoint='products')
api.add_resource(SubCategories, '/categories/<int:category_id>/subcategories', endpoint='subcategories')
api.add_resource(_Product, '/products/<int:product_id>', endpoint='product')
api.add_resource(_SubCategory, '/subcategories/<int:sub_category_id>', endpoint='subcategory')
api.add_resource(Skus, '/products/<int:product_id>/skus', endpoint='skus')
api.add_resource(SpecificSku, '/skus/<int:sku_id>', endpoint='sku')
