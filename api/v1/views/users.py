#!/usr/bin/python3
""" Users view """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_user(user_id=None):
    """ Retrieves the list of all Users or just one User """
    if user_id is None:
        users = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(users)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ delete an User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ create a User """
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    if 'email' not in req:
        abort(400, {'Missing email'})
    if 'password' not in req:
        abort(400, {'Missing password'})
    user = User(**req)
    user.save()
    return user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id=None):
    """ update an User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    for key, val in req.items():
        if key not in ('id', 'email', 'created_at', 'updates_at'):
            setattr(user, key, val)
    user.save()
    return user.to_dict()
