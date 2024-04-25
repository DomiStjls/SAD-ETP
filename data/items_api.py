import flask
from flask import jsonify, make_response, request

from . import db_session
from .item import Item

blueprint = flask.Blueprint(
    'items_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/item/<item_id>', methods=['GET'])
def info_all(item_id):
    db_sess = db_session.create_session()
    try:
        item = db_sess.query(Item).get(item_id)
        return jsonify(item.to_dict())
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/item', methods=['GET'])
def get_jobs():
    try:
        db_sess = db_session.create_session()
        items = db_sess.query(Item).all()
        return jsonify({'items': [item.to_dict() for item in items]})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/item', methods=['POST'])
def create_item():
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['name', 'description', 'category', 'maker', 'price', 'photo']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        item = Item(
            name=request.json['name'],
            description=request.json['description'],
            category=request.json['category'],
            photo=request.json['photo'],
            maker=request.json['maker'],
            price=request.json['price'],
        )
        db_sess.add(item)
        db_sess.commit()
        return jsonify({'id': item.id})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        db_sess = db_session.create_session()
        item = db_sess.query(Item).get(item_id)
        if not item:
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess.delete(item)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/item/<item_id>', methods=['PUT'])
def edit_job(item_id):
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['name', 'description', 'category', 'maker', 'price', 'photo']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess = db_session.create_session()
        item = db_sess.query(Item).get(item_id)
        if not item:
            return make_response(jsonify({'error': 'Bad request'}), 400)
        item.name = request.json['name']
        item.description = request.json['description']
        item.category = request.json['category']
        item.maker = request.json['maker']
        item.price = request.json['price']
        item.photo = request.json['photo']
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)
