from data import db_session
from data.item import Item

try:
    # os.system('type nul > db/shop.db')

    db_session.global_init("db/shop.db")
    db_sess = db_session.create_session()
    items = [
        (1, "q1", "w1", "e1", "photo1", 521),
        (2, "q2", "w2", "e2", "photo2", 522),
        (3, "q3", "w3", "e3", "photo3", 523),
        (4, "q4", "w4", "e4", "photo4", 524),
        (5, "q5", "w5", "e5", "photo5", 525),
    ]
    for (id, category, name, description, photo, price) in items:
        item = Item(
            name=name,
            category=category,
            description=description,
            photo=photo,
            price=price,
        )
        db_sess.add(item)

    db_sess.commit()

except Exception as e:
    print(e)
