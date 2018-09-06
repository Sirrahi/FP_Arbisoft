from triumph import app
from flask import render_template
from triumph.models import Category, Item

categories = Category.query.all()

@app.route('/')
@app.route('/categories')
def index():
    return render_template('index.html', title='Triumph', categories=categories)


@app.route('/categories/<int:category_id>/products')
def category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    name = category.name
    products = []

    for product in category.items:
        products.append(product)

    return render_template('category.html', name=name, products=products, categories=categories)


@app.route('/products/<int:product_id>')
def product(product_id):
    product = Item.query.filter_by(id=product_id).first()

    return render_template('product.html', product=product, categories=categories)