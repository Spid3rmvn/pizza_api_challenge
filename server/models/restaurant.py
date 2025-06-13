from server.app import db
from sqlalchemy.orm import validates


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    # Relationship with RestaurantPizza (one-to-many)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')

    def to_dict(self, include_pizzas=False):
        restaurant_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

        if include_pizzas:
            restaurant_dict['pizzas'] = [
                {
                    'id': rp.pizza.id,
                    'name': rp.pizza.name,
                    'ingredients': rp.pizza.ingredients
                }
                for rp in self.restaurant_pizzas
            ]

        return restaurant_dict

    def __repr__(self):
        return f'<Restaurant {self.name}>'