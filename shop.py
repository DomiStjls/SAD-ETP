from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.app_context().push()

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    photo = db.Column(db.String)
    price = db.Column(db.Integer, nullable=False)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
