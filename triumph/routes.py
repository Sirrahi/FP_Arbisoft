from triumph import app
from flask import render_template, abort
from triumph.models import Category, Product, SubCategory,Sku


@app.route('/triumph')
def index():
    categories = Category.query.all()

    return render_template('index.html', title='Home', categories=categories)


@app.route('/triumph/categories/<int:category_id>/sub_categories')
def category(category_id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=category_id).first()

    if category is None:
        abort(404)

    return render_template('category.html', title=category.name, categories=categories, category=category)


@app.route('/triumph/categories/<int:category_id>/sub_categories/<int:sub_category_id>')
def sub_category(category_id, sub_category_id):
    categories = Category.query.all()
    sub_category = SubCategory.query.get(sub_category_id)
    category = Category.query.get(category_id)

    if sub_category is None:
        abort(404)

    products = Product.query.filter_by(sub_category_id=sub_category_id).all()

    return render_template('sub_category.html', title=sub_category.name, sub_category=sub_category,
                           category=category, products=products, categories=categories)


@app.route('/triumph/categories/<int:category_id>/sub_categories/<int:sub_category_id>/products/<int:product_id>')
def product(category_id, sub_category_id, product_id):
    categories = Category.query.all()
    product = Product.query.filter_by(id=product_id).first()

    if product is None:
        abort(404)

    return render_template('product.html', title=product.name, product=product, categories=categories)


@app.route('/triumph/categories/<int:category_id>/sub_categories'
           '/<int:sub_category_id>/products/<int:product_id>/sku/<int:sku_id>')
def sku(category_id, sub_category_id, product_id, sku_id):
    categories = Category.query.all()
    sku = Sku.query.get(sku_id)

    if sku is None:
        abort(404)

    return render_template('sku.html', title=sku.color, sku=sku, categories=categories)
