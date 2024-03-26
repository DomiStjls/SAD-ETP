from flask import *
from data import db_session
from data.item import Item

DEBUG = True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


def main():
    db_session.global_init('db/shop.db')
    app.run(port=8080, host='127.0.0.1', debug=DEBUG)


if __name__ == '__main__':
    main()
