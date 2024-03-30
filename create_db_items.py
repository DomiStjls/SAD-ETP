# тут будет код который загрузит информацию из prices.xlsx в базу данных

import os

from data import db_session
from data.user import User
from data.item import Item

try:
    # os.system('type nul > db/shop.db')

    db_session.global_init("db/shop.db")
    db_sess = db_session.create_session()
    with open("prices.csv", encoding='utf-8') as f:
        r = f.readlines()[1:]
        for i in range(16):
            s = r[i].split(";")
            category = s[0]
            name = s[5]
            description = s[9]
            photo = s[12]
            price = int(s[7].split(',')[0])
            item = Item(name=name,category=category,description=description,photo=photo,price=price)
            db_sess.add(item)


    db_sess.commit()

except Exception as e:
    print(e)
