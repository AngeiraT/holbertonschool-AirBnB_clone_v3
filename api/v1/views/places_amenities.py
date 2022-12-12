#!/usr/bin/python3
""" Places_Amenities view """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities_get(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get('Place', place_id)
    amenities_list = []
    if place is None:
        abort(404)
    for amenity in place.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_amenity_delete(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.delete(amenity)
    storage.save()
    return {}


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def place_amenity_post(place_id, amenity_id):
    """Creates an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    place.amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
