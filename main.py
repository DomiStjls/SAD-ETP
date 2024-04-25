from flask import *
from flask_login import *

from data import db_session, items_api, orders_api
from data.item import Item
from data.loginform import LoginForm
from data.order import Order
from data.signupform import SignUpForm
from data.user import User

DEBUG = False

ADMINS = [1, 2]

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandex_lyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """эта функция проверяет регистрацию пользователя на сайте и возвращает его

    Args:
        user_id (integer): номер пользователя

    Returns:
        пользователя, взятого из бд
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    """эта функция регестрирует нового пользователи и дает войти уже существующему

    Returns:
        страницу с авторизацией или главную страницу магазина при удачном входе
    """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # переход на главную старницу
            return redirect(session["url"])
        # неудачный вход
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
        # авторизация
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            db_sess = db_session.create_session()
            user = User(name=form.name.data, surname=form.surname.data, age=form.age.data, email=form.email.data,
                        cart="")
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
        except Exception as e:
            return render_template("signup.html", message="Аккаунт с этой почтой уже есть", title="Регистрация",
                                   form=form)
    return render_template("signup.html", title="Регистрация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(session["url"])


@app.route("/")
def index():
    """главная страница с товарами

    Returns:
        страницу с товарами
    """
    db_sess = db_session.create_session()
    data = db_sess.query(Item).all()
    session["url"] = "/"
    return render_template("index.html", data=data)


@app.route("/about")
def about():
    """страница с текстом о нас

    Returns:
        страница о нас
    """
    return render_template("about.html")


@app.route("/item/<id>")
def item(id):
    """страница о товаре с описанием, крупной картинкой и возможностью добавить в корзину

    Args:
        id (integer): номер товара

    Returns:
        страницу с товаром
    """
    try:
        # переход на страницу с товаром
        session["url"] = f"/item/{id}"
        db_sess = db_session.create_session()
        q = db_sess.query(Item).filter(Item.id == id).first()
        # преобразование товара в словарь со свойствами
        product = {
            "id": q.id,
            "name": q.name,
            "description": q.description,
            "category": q.category,
            "price": q.price,
            "photo": q.photo,
            'maker': q.maker,
        }
        #  проверка на авторизацию
        if current_user.is_authenticated:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            cart = [i.split(":")[0] for i in user.cart.split(";")]


        else:
            cart = []

        # если пользователь авторизован на сайте, мы ищем его корзину
        # далее проверяем, есть ли товар, который он собирается посмотреть в корзине
        # если есть, то на странице с товаром будет написано, что товар уже в корзине
        # если нет, то на странице с товаром будет написано, что товар можно добавить в корзину
        # это сделано через передачу параметра (id in cart)

        return render_template(
            "item.html", title=product["name"], product=product, cart=(id in cart)
        )
    except Exception:
        return make_response(jsonify({"error": "Bad request"}), 400)


@app.route('/search', methods=["GET"])
def search():
    """поиск товара

    Returns:
        страницу с найденными товарами
    """
    try:
        session["url"] = "/search"
        # берем из формы параметры для фильтрации
        category = request.args.get("category")
        db_sess = db_session.create_session()
        if category == 'Comp':
            category = 'Компьютерная техника'
            q = db_sess.query(Item).filter(Item.category == category).all()
        elif category == 'Mobil':
            category = 'Мобильные и связь'
            q = db_sess.query(Item).filter(Item.category == category).all()
        else:
            category = ''
            q = db_sess.query(Item).all()
        name = request.args.get("name")
        maker = request.args.get("maker")
        # сначала берем из бд только записи в нужной нам категории
        # теперь уже отбираем нужные нам
        data = [el for el in q if name.lower() in el.name.lower() and maker.lower() in el.maker.lower()]
        return render_template('search.html', data=data, total=len(data))
    except Exception as e:
        print(e)
        # в случае ошибки пользователь просто останется на главной странице
        return redirect('/')



@app.route("/cart")
def cart():
    """корзина пользователя

    Returns:
        сраница с товарами в корзине
    """
    session["url"] = "/cart"
    if not current_user.is_authenticated:
        # если в корзину перейдет пользователь без регистрации,
        # его переправит на страницу с регистрацией
        return redirect("/login")
    db_sess = db_session.create_session()
    #  находим нашего пользователя и его корзину
    q = db_sess.query(User).filter(User.id == current_user.id).first()
    products = []
    # считываем все товары из корзины, чтобы показать их
    for id, n in ([tuple(i.split(":")) for i in q.cart.split(";")] if q.cart else []):
        n = int(n)
        w = db_sess.query(Item).filter(Item.id == id).first()
        products.append(
            {
                "id": w.id,
                "name": w.name,
                "number": n,
                "category": w.category,
                "price": w.price,
                "photo": w.photo,
            }
        )
    return render_template(
        "cart.html", products=products, total=sum(map(lambda x: x["price"], products))
    )


@app.route("/addcart/<id>", methods=["GET"])
def addcart(id):
    # def code(dic):
    #     return ";".join([f"{k}:{v}" for k, v in dic.items()])
    #
    # def decode(s):
    #     s = [tuple(i.split(':')) for i in list(s.split(";"))]
    #     d = {}
    #     for i in s:
    #         d[i[0]] = int(i[1])
    #     return d
    """добавление товара в карзину

    Args:
        id (integer): номер товара, который мы хотим добавить

    Returns:
        в зависимости от того, откуда пользователь добавляет товар, его перенаправит или на страницу с товаром,
        или на главную
    """
    try:
        n = int(request.args.get("number")) if request.referrer.split('/')[-2] == 'item' else 1
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # добавление товара в корзину
        s = user.cart
        s += f";{id}:{n}"
        if s[0] == ";":
            s = s[1:]
        user.cart = s
        db_sess.commit()
        return redirect(f"/item/{id}") if request.referrer.split('/')[-2] == 'item' else redirect("/")
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Bad request"}), 400)


@app.route('/order', methods=['POST'])
def order():
    """форма для оформления заказа

    Returns:
        сраница с формой для оформления заказа
    """
    try:
        if not current_user.is_authenticated:
            return make_response(jsonify({"error": "Bad request"}), 400)
        db_sess = db_session.create_session()
        data = dict(request.form)
        address = data.get("address", None)
        phone = data.get("phone", None)
        if not address or not phone:
            raise ValueError
        del data['address']
        del data['phone']
        s = ""
        for key, value in data.items():
            id = int(key[7:])
            n = int(value)
            s += f"{id}:{n};"
        s = s[:-1]
        order = Order(client=current_user.id, order=s, address=address, phone=phone)
        db_sess.add(order)
        db_sess.commit()
        q = db_sess.query(User).filter(User.id == current_user.id).first()
        q.cart = ""
        db_sess.commit()
        return render_template('order.html', success=True)
    except Exception as e:
        return render_template('order.html', success=False)


@app.route('/admin')
def admin():
    """страница администратора

    Returns:
        сраница с заказами
    """
    if not current_user.is_authenticated:
        return make_response(jsonify({"error": "Unathorized Access"}), 401)
    if not current_user.id in ADMINS:
        return make_response(jsonify({"error": "Forbidden"}), 403)
    db_sess = db_session.create_session()
    orders = []
    for order in db_sess.query(Order).all():
        o = []
        for id, n in ([tuple(i.split(":")) for i in order.order.split(";")] if order.order else []):
            q = db_sess.query(Item).filter(Item.id == id).first()
            o.append({'id': id, 'n': n, 'name': q.name, 'category': q.category})
        orders.append({'id': order.id, 'address': order.address, "phone": order.phone, 'name': 'n', 'surname': 's',
                       'order': o})
    return render_template('admin.html', orders=orders)


@app.route('/deleteorder/<order_id>')
def deleteorder(order_id):
    if not current_user.is_authenticated:
        return make_response(jsonify({"error": "Unathorized Access"}), 401)
    if not current_user.id in ADMINS:
        return make_response(jsonify({"error": "Forbidden"}), 403)
    db_sess = db_session.create_session()
    item = db_sess.query(Order).get(order_id)
    if not item:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess.delete(item)
    db_sess.commit()
    return redirect('/admin')


def main():
    """функция для запуска локального сервера и подключения к дб
    """
    db_session.global_init("db/shop.db")
    app.register_blueprint(items_api.blueprint)
    app.register_blueprint(orders_api.blueprint)
    app.run(port=8080, host="127.0.0.1", debug=DEBUG)


if __name__ == "__main__":
    main()
