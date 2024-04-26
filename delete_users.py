from data import db_session
from data.user import User
from data.item import Item

db_session.global_init("db/shop.db")
db_sess = db_session.create_session()
for i in db_sess.query(User).all():
    db_sess.delete(i)
db_sess.commit()