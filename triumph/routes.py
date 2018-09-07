from flask import render_template, abort, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from triumph import app, db
from triumph.forms import LoginForm, RegistrationForm, CartForm
from triumph.models import Category, Product, SubCategory, Sku, User, CartItem


@app.route('/')
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
    category = Category.query.get(category_id)
    sub_category = SubCategory.query.get(sub_category_id)
    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    return render_template('product.html', title=product.name, product=product,
                           categories=categories, category=category, sub_category=sub_category)


@app.route('/triumph/categories/<int:category_id>/sub_categories'
           '/<int:sub_category_id>/products/<int:product_id>/sku/<int:sku_id>', methods=['GET'])
def sku(category_id, sub_category_id, product_id, sku_id):
    categories = Category.query.all()
    category = Category.query.get(category_id)
    sub_category = SubCategory.query.get(sub_category_id)
    product = Product.query.get(product_id)
    sku = Sku.query.get(sku_id)
    title = sku.product.name + ' ' + sku.color

    if sku is None:
        abort(404)

    return render_template('sku.html', title=title, sku=sku, categories=categories,
                           category=category, sub_category=sub_category, product=product)


@app.route('/triumph/login', methods=['GET', 'POST'])
def login():
    categories = Category.query.all()
    form = LoginForm()

    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html', title='Sign In', form=form, categories=categories)

    else:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form, categories=categories)


@app.route('/triumph/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/triumph/registration', methods=['GET', 'POST'])
def register():
    categories = Category.query.all()
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', title='Registration', categories=categories, form=form)

    else:
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('index'))
        return render_template('register.html', title='Registration', categories=categories, form=form)


@app.route('/triumph/categories/<int:category_id>/sub_categories'
           '/<int:sub_category_id>/products/<int:product_id>/sku/<int:sku_id>/addtocart', methods=['GET', 'POST'])
@login_required
def addtocart(category_id, sub_category_id, product_id, sku_id):
    categories = Category.query.all()
    form = CartForm(request.form)
    sku = Sku.query.get(sku_id)
    user = User.query.filter_by(username=current_user.username).first()
    title = sku.product.name + ' ' + sku.color
    if request.method == 'GET':
        return render_template('addtocart.html', title=title, categories=categories, form=form, sku=sku)

    else:
        if form.validate_on_submit():
            cartitem = CartItem(name=sku.product.name, color=sku.color, size=sku.size, price=sku.price,
                                currency=sku.currency, image_url=sku.image_urls[0].url, quantity=form.quantity.data)
            db.session.add(cartitem)
            user.cartitems.append(cartitem)
            db.session.commit()
            flash('Item added to cart')
            return redirect(url_for('sku', title=title, category_id=category_id, sub_category_id=sub_category_id,
                                    product_id=product_id, sku_id=sku_id))

        return render_template('addtocart.html', categories=categories, form=form, sku=sku)


@app.route('/triumph/cart')
@login_required
def cart():
    categories = Category.query.all()
    form = CartForm()
    user = User.query.filter_by(username=current_user.username).first()

    return render_template('cart.html', title='My Cart', categories=categories, form=form, user=user)


@app.route('/triumph/cart/<int:cartitem_id>')
def rmcartitem(cartitem_id):
    categories = Category.query.all()
    form = CartForm()
    cartitem = CartItem.query.get(cartitem_id)
    db.session.delete(cartitem)
    db.session.commit()
    user = User.query.filter_by(username=current_user.username).first()

    return render_template('cart.html', categories=categories, form=form, user=user)
