from flask import *
from flask_login import *

from data import db_session
from data.item import Item
from data.loginform import LoginForm
from data.user import User

DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def main():
    db_sess = db_session.create_session()
    data = db_sess.query(Item).all()
    print(data)
    return render_template("index.html", data=data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/item/<id>")
def item(id):
    try:
        db_sess = db_session.create_session()
        q = db_sess.query(Item).filter(Item.id == id).first()
        product = {
            "id": q.id,
            "name": q.name,
            "description": q.description,
            "category": q.category,
            "price": q.price,
        }
        return render_template("item.html", title=product["name"], product=product)
    except Exception as e:
        return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route("/cart")
def cart():
    products = [
        {"name": "q", "category": "w", "price": 52},
        {"name": "q", "category": "w", "price": 52},
        {"name": "q", "category": "w", "price": 52},
    ]
    return render_template("cart.html", products=products, total=sum(map(lambda x: x["price"], products)))


@app.route("/addcart/<id>", methods=["GET", "POST"])
def addcart(id):
    def code(dic):
        return ";".join([f"{k}:{v}" for k, v in dic.items()])

    def decode(s):
        s = [tuple(i.split(':')) for i in list(s.split(";"))]
        d = {}
        for i in s:
            d[i[0]] = int(i[1])
        return d

    try:
        print(request.form.number)
    except Exception as e:
        return make_response(jsonify({'error': 'Bad request'}), 400)


def main():
    db_session.global_init('db/shop.db')
    app.run(port=8080, host='127.0.0.1', debug=DEBUG)


if __name__ == '__main__':
    main()
