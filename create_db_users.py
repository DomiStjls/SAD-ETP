# создание учетных записей (для тестирования)

import os

from data import db_session
from data.user import User
from data.item import Item

try:
    # linux (glitch)
    os.system(':> db/shop.db')
    # windows
    # os.system('type nul > db/shop.db')

    db_session.global_init("db/shop.db")
    db_sess = db_session.create_session()

    u1 = User(name="Максим", surname="Харламов", age=52, email="1@ya.ru")
    u1.set_password('password1')

    u2 = User(name="Даша", surname="Шевченко", age=5, email="2@ya.ru")
    u2.set_password('password2')

    u3 = User(name="Милана", surname="Семенова", age=99, email="3@ya.ru")
    u3.set_password('password3')

    u4 = User(name="Ярослав", surname="Серов", age=4, email="4@ya.ru")
    u4.set_password('password4')

    u5 = User(name="Александр", surname="Шадрин", age=69, email="5@ya.ru")
    u5.set_password('password5')

    db_sess.add(u1)
    db_sess.add(u2)
    db_sess.add(u3)
    db_sess.add(u4)
    db_sess.add(u5)
    db_sess.commit()

except Exception as e:
    print(e)
