#!/usr/bin/python3
""" Places view """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_city(city_id=None, place_id=None):
    """ Retrieves the list of all cities or just one City """
    if city_id is None:
        cities = [city.to_dict() for city in storage.all("City").values()]
        return jsonify(cities)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/places', methods=['GET'], strict_slashes=False)
@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_place(place_id=None):
    """ Retrieves the list of all places or just one Place """
    if place_id is None:
        places = [place.to_dict() for place in storage.all("Place").values()]
        return jsonify(places)
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ delete a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_place():
    """ create a Place """
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    if 'name' not in req:
        abort(400, {'Missing name'})
    if 'user_id' not in req:
        abort(400, {'Missing user_id'})
    place = Place(**req)
    place.save()
    return place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id=None):
    """ update a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    try:
        req = request.get_json()
    except:
        req = None
    if req is None:
        abort(400, {'Not a JSON'})
    for key, val in req.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updates_at'):
            setattr(place, key, val)
    place.save()
    return place.to_dict()
