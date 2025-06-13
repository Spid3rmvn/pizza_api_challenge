from flask import Blueprint, jsonify
from server.app import db
from server.models.restaurant import Restaurant

restaurant_bp = Blueprint('restaurants', __name__)


@restaurant_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    """Get all restaurants"""
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])


@restaurant_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    """Get a single restaurant with its pizzas"""
    restaurant = Restaurant.query.get(id)

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    return jsonify(restaurant.to_dict(include_pizzas=True))


@restaurant_bp.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    """Delete a restaurant and all related RestaurantPizzas"""
    restaurant = Restaurant.query.get(id)

    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return '', 204