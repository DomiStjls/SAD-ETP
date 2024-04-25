import flask
from flask import jsonify, make_response, request

from . import db_session
from .order import Order

blueprint = flask.Blueprint(
    'orders_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/order/<order_id>', methods=['GET'])
def info_all(order_id):
    db_sess = db_session.create_session()
    try:
        item = db_sess.query(Order).get(order_id)
        return jsonify(item.to_dict())
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/order', methods=['GET'])
def get_jobs():
    try:
        db_sess = db_session.create_session()
        items = db_sess.query(Order).all()
        return jsonify({'items': [item.to_dict() for item in items]})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)


@blueprint.route('/api/order/<order_id>', methods=['DELETE'])
def delete_item(order_id):
    try:
        db_sess = db_session.create_session()
        item = db_sess.query(Order).get(order_id)
        if not item:
            return make_response(jsonify({'error': 'Bad request'}), 400)
        db_sess.delete(item)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)
