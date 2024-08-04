from flask import Flask, render_template, redirect, request
from flask import make_response, jsonify
from data import db_session

from data.users import User
from data.products import Product
from data.product_comments import ProductComment
from data.photo import Photo
from data.multiproducts import MultiProduct
from data.orders import Order

from forms.login import LoginForm
from forms.register import RegisterForm, EditForm
from forms.product import ProductForm
from forms.order import OrderForm


from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import Api

from flask_mail import Mail, Message

import os
import json

from datetime import datetime


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def not_authenticated(*args, **kwargs):
    if current_user.is_authenticated:
        return False
    return True


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


def main():
    db_session.global_init("db/cumzon.sqlite")
    app.run(debug=True)

    print('nice')


@app.route('/')
def index():
    if not_authenticated():
        return redirect('/preview')

    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter((
        Product.seller_id != current_user.id) & (Product.count != 0)).all()

    counts = [db_sess.query(MultiProduct).filter((MultiProduct.product_id == product.id) & (
        MultiProduct.user_id == current_user.id)).first() for product in products]

    counts = [counts[i].count if counts[i]
              is not None else 0 for i in range(len(counts))]

    return render_template('index.html', title='CUMZONE', products=products, counts=counts)


@app.route('/preview')
def preview():
    return render_template('preview.html', title='Обзор')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # форма регистрации
    db_sess = db_session.create_session()

    if len(db_sess.query(User).all()) > 10:
        return redirect('/preview')
    
    if form.validate_on_submit():
        # проверка на корректность введенных данных
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть, выберите другую почту")

        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким никнеймом уже есть")

        # новый пользователь
        user = User(
            email=form.email.data,
            nickname=form.nickname.data
        )

        # пароль
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        # аватар
        f = form.profile_image.data
        if f:
            f.save(fr'static/profile_images/{user.id}{f.filename[-4:]}')
            user.profile_image = fr'/static/profile_images/{user.id}{f.filename[-4:]}'

        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # форма авторизации
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход из системы
@app.route('/logout')
def logout():
    if not_authenticated():
        return redirect('/preview')
    logout_user()
    return redirect("/")


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    multiproduct = MultiProduct(
        user_id=current_user.id, count=1, product_id=product_id)
    db_sess.add(multiproduct)
    db_sess.commit()
    return ""


@app.route('/change_count/<int:product_id>/<string:type_>', methods=['POST'])
def change_count(product_id, type_):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    multiproduct = db_sess.query(MultiProduct).filter(
        (MultiProduct.user_id == current_user.id) & (MultiProduct.product_id == product_id)).first()
    if type_ == 'plus':
        multiproduct.count += 1
    else:
        multiproduct.count -= 1
    if multiproduct.count == 0:
        db_sess.delete(multiproduct)
    db_sess.commit()

    return ""


@app.route('/products/<category>')
def products_category_page(category):
    if not_authenticated():
        return redirect('/preview')

    db_sess = db_session.create_session()
    if category == 'all':
        products = db_sess.query(Product).filter(
            Product.seller_id != current_user.id).all()
    else:
        products = db_sess.query(Product).filter(
            (Product.category == category) & (Product.seller_id != current_user.id) & (Product.count != 0)).all()

    counts = [db_sess.query(MultiProduct).filter((MultiProduct.product_id == product.id) & (
        MultiProduct.user_id == current_user.id)).first() for product in products]

    counts = [counts[i].count if counts[i]
              is not None else 0 for i in range(len(counts))]

    cat = 'Все товары'
    match category:
        case 'all':
            cat = 'Все товары'
        case 'block':
            cat = 'Блоки'
        case 'resource':
            cat = 'Ресурсы'
        case 'building':
            cat = 'Постройки'
        case 'job':
            cat = 'Услуги'
        case 'other':
            cat = 'Всякая хуйня для лохов ну и тд тп'

    return render_template('category.html', title='CUMZONE', products=products, counts=counts, category=cat)


@app.route('/product/<int:product_id>')
def product_page(product_id):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    multiproduct = db_sess.query(MultiProduct).filter(
        (MultiProduct.user_id == current_user.id) & (MultiProduct.product_id == product_id)).first()
    count = 0
    if multiproduct:
        count = multiproduct.count

    cat = 'Все товары'
    match product.category:
        case 'all':
            cat = 'Все товары'
        case 'blocks':
            cat = 'Блоки'
        case 'resources':
            cat = 'Ресурсы'
        case 'buildings':
            cat = 'Постройки'
        case 'jobs':
            cat = 'Услуги'
        case 'other':
            cat = 'Всякая хуйня для лохов ну и тд тп'

    if any(current_user.id == comment.user.id for comment in product.comments) or product.seller.id == current_user.id:
        can_make_comment = False
    else:
        can_make_comment = True

    return render_template('product_page.html', title='CUMZONE', product=product, count=count, category=cat, can_make_comment=can_make_comment, date_now=datetime.strftime(datetime.now(), r'%Y-%m-%d'))


@app.route('/save_comment548548/<int:product_id>/<int:user_id>/<comment_text>', methods=['POST'])
def save_comment(product_id, user_id, comment_text):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    comment = ProductComment(text=comment_text, author_id=user_id, product_id=product_id)
    db_sess.add(comment)
    db_sess.commit()
    return ""


@app.route('/store/my', methods=['POST', 'GET'])
def store():
    if not_authenticated():
        return redirect('/preview')
    form = ProductForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():

        if form.count.data <= 0:
            return render_template('store.html',
                                   message="Бро, товара нету? А если найду! вводи давай",
                                   form=form, hideform=False)

        product = Product(
            name=form.name.data,
            description=form.description.data,
            seller_id=current_user.id,
            price=form.price.data,
            count=form.count.data,
            category=form.category.data
        )

        db_sess.add(product)
        db_sess.commit()
        product = db_sess.query(Product).filter(
            Product.name.like(form.name.data)).first()

        for number, file in enumerate(form.screenshots.data):
            filename = file.filename

            try:
                os.mkdir(fr'static/products/{product.name}/')
            except Exception:
                pass
            try:
                os.mkdir(fr'static/products/{product.name}/photos/')
            except Exception:
                pass

            file.save(
                fr'static/products/{product.name}/photos/{number + 1}.{filename[-3:]}')
            photo = Photo(path=fr'/static/products/{product.name}/photos/{number + 1}.{filename[-3:]}',
                          parent_product=product.id)
            product.photos.append(photo)

        db_sess.commit()
        return redirect(f'/store/my')

    user_id = current_user.id
    title = 'Мой магазин'

    orders = db_sess.query(Order).filter(Order.seller_id == user_id).all()
    prices = [sum([db_sess.query(Product).filter(Product.id == multiproduct.product_id).first().price * multiproduct.count for multiproduct in order.products]) for order in orders]

    products = db_sess.query(Product).filter(
        Product.seller_id == user_id).all()

    counts = [db_sess.query(MultiProduct).filter((MultiProduct.product_id == product.id) & (
        MultiProduct.user_id == current_user.id)).first() for product in products]

    counts = [counts[i].count if counts[i]
              is not None else 0 for i in range(len(counts))]

    return render_template('store.html', title=title, products=products, counts=counts, orders_count=current_user.orders_count, form=form, hideform=True, orders=orders, prices=prices)


@app.route('/delite_product548548/<int:product_id>', methods=['POST'])
def delte_product(product_id):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    db_sess.delete(product)
    photos = db_sess.query(Photo).filter(
        Photo.parent_product == product_id).all()
    for photo in photos:
        db_sess.delete(photo)
    db_sess.commit()

    return ""


@app.route('/edit_product548548/<int:product_id>/<name>/<description>/<int:price>/<int:count>', methods=['POST'])
def edit_product(product_id, name, description, price, count):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    product.name = name
    product.description = description
    product.price = price
    product.count = count
    db_sess.commit()

    return ""


@app.route('/cart')
def cart():
    if not_authenticated():
        return redirect('/preview')
    db_sess = db_session.create_session()

    if current_user.cart:
        counts = current_user.cart

        all_price = 0
        products = []
        for count in counts:
            product = db_sess.query(Product).filter(
                Product.id == count.product_id).first()
            products += [product]
            all_price += product.price * count.count
        counts = [counts[i].count if counts[i]
                  is not None else 0 for i in range(len(counts))]
    else:
        products = []
        counts = []
        all_price = 0

    return render_template('cart.html', title='Корзина', products=products, counts=counts, all_price=all_price)


@app.route('/make_order', methods=['POST', 'GET'])
def make_order():
    if not_authenticated():
        return redirect('/preview')
    form = OrderForm()
    db_sess = db_session.create_session()

    if form.validate_on_submit():
        point = form.point.data
        nickname = current_user.nickname
        with open('storage.json', encoding='uft-8') as file:
            storage = json.load(file)
            cases = storage[point]
            
            free_cases = [i for i in range(len(cases)) if cases[i]]


        products = db_sess.query(MultiProduct).filter(
            MultiProduct.user_id == current_user.id).all()

        seller_products = {}
        for multiproduct in products:
            product = db_sess.query(Product).filter(
                Product.id == multiproduct.product_id).first()
            product.count -= multiproduct.count
            seller_id = product.seller_id
            if seller_id not in seller_products:
                seller_products[seller_id] = [multiproduct]
            else:
                seller_products[seller_id] += [multiproduct]

        date = datetime.strftime(datetime.now(), r"%d.%m.%y %H:%M")
        for seller_id, multiproducts in seller_products.items():
            order = Order(nickname=nickname, seller_id=seller_id,
                          point=point, products=multiproducts, create_time=date, storage=free_cases[0] + 1)
            del free_cases[0]
            db_sess.add(order)

        db_sess.commit()
        products = db_sess.query(MultiProduct).filter(
            MultiProduct.user_id == current_user.id).all()
        for multiproduct in products:
            multiproduct.user_id = None
            product = multiproduct.product

            needs_change_multiproducts = db_sess.query(MultiProduct).filter(
                MultiProduct.product_id == product.id).all()
            for m in needs_change_multiproducts:
                m.count = max(m.count, product.count)

        db_sess.commit()

        cases = [1 if i in free_cases else 0 for i in range(len(cases))]
        storage[point] = cases

        with open('storage.json', encoding='uft-8') as file:
            json.dump(storage, file)

        return render_template('order_has_been_created.html')

    if current_user.cart:
        counts = current_user.cart

        all_price = 0
        products = []
        for count in counts:
            product = db_sess.query(Product).filter(
                Product.id == count.product_id).first()
            products += [product]
            all_price += product.price * count.count
        counts = [counts[i].count if counts[i]
                  is not None else 0 for i in range(len(counts))]
    else:
        products = []
        counts = []
        all_price = 0

    return render_template('make_order.html', title='Оформление заказа', products=products, counts=counts, all_price=all_price, form=form)



@app.route('/change_order_status548548/<int:order_id>/<status>', methods=['POST'])
def change_order_status(order_id, status):
    db_sess = db_session.create_session()
    if not_authenticated():
        return redirect('/preview')
    order = db_sess.query(Order).filter(Order.id == order_id).first()
    order.status = status

    if status == 'Оплачен и завершён':
        db_sess.query(User).filter(User.nickname ==
                                   order.nickname).first().orders_bougth += 1
        
        with open('storage.json', encoding='utf-8') as file:
            storage = json.load(file)
            storage[order.point][order.storage - 1] = 1
            json.dump(storage, file)
            
        db_sess.delite(order)
        

    db_sess.commit()
    return ""

@app.route('/profile/edit', methods=['POST', 'GET'])
def profile_edit():
    if not_authenticated():
        return redirect('/preview')
    db_sess = db_session.create_session()
    form = EditForm()
    form.nickname.data = current_user.nickname

    if form.validate_on_submit():

        if db_sess.query(User).filter((User.nickname == form.nickname.data) & (User.nickname != current_user.nickname)).first() is not None:
            return render_template('profile_edit.html', title='Редактирование профиля',
                                   form=form,
                                   message="Пользователь с таким никнеймом уже есть")

        current_user.nickname = form.nickname.data

        # аватар
        f = form.profile_image.data
        if f:
            f.save(
                fr'static/profile_images/{current_user.id}{f.filename[-4:]}')
            current_user.profile_image = fr'/static/profile_images/{current_user.id}{f.filename[-4:]}'

        db_sess.commit()
        return redirect('/profile')

    return render_template('profile_edit.html', title='Редактирование профиля', form=form)

@app.route('/profile')
def profile():
    if not_authenticated():
        return redirect('/preview')
    db_sess = db_session.create_session()
    orders = db_sess.query(Order).filter(Order.nickname == current_user.nickname).all()
    prices = [sum([db_sess.query(Product).filter(Product.id == multiproduct.product_id).first().price * multiproduct.count for multiproduct in order.products]) for order in orders]

    return render_template('profile.html', title='Профиль', orders=orders, prices=prices)

if __name__ == '__main__':
    main()
