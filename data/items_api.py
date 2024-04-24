import flask
from flask import jsonify, make_response

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
        return jsonify({'jobs': [item.to_dict() for item in items]})
    except Exception as e:
        return make_response(jsonify({"error": "Bad request"}), 400)
