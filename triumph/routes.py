from triumph import app
from flask import render_template
from triumph.models import Category, Product, SubCategory


@app.route('/categories')
def index():
    categories = Category.query.all()

    return render_template('index.html', title='Home', categories=categories)


@app.route('/categories/<int:category_id>/sub_categories')
def category(category_id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=category_id).first()
    name = category.name

    return render_template('category.html', title=name, name=name, categories=categories, category=category)


@app.route('/sub_categories/<int:sub_category_id>')
def sub_category(sub_category_id):
    categories = Category.query.all()
    name = SubCategory.query.get(sub_category_id).name
    products = Product.query.filter_by(sub_category_id=sub_category_id).all()

    return render_template('sub_category.html', titele=name, name=name, products=products, categories=categories)


@app.route('/products/<int:product_id>')
def product(product_id):
    categories = Category.query.all()
    product = Product.query.filter_by(id=product_id).first()

    return render_template('product.html', title=product.name, product=product, categories=categories)
