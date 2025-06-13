from server.app import create_app, db
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza


def seed_data():
    app = create_app()

    with app.app_context():
        # Clear existing data
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()

        # Create Restaurants
        restaurants = [
            Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 4th Floor"),
            Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road"),
            Restaurant(name="Kiki's Pizza", address="Kilimani, Dennis Pritt Road")
        ]

        # Create Pizzas
        pizzas = [
            Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese"),
            Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"),
            Pizza(name="California",
                  ingredients="Dough, Sauce, Ricotta, Red peppers, Goat cheese, Italian sausage, Mushrooms"),
            Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Fresh Mozzarella, Basil"),
            Pizza(name="Hawaiian", ingredients="Dough, Tomato Sauce, Cheese, Ham, Pineapple")
        ]

        # Add to database
        for restaurant in restaurants:
            db.session.add(restaurant)

        for pizza in pizzas:
            db.session.add(pizza)

        db.session.commit()

        # Create RestaurantPizzas (sample relationships)
        restaurant_pizzas = [
            RestaurantPizza(price=10, restaurant_id=1, pizza_id=1),
            RestaurantPizza(price=15, restaurant_id=1, pizza_id=2),
            RestaurantPizza(price=12, restaurant_id=2, pizza_id=1),
            RestaurantPizza(price=18, restaurant_id=2, pizza_id=3),
            RestaurantPizza(price=14, restaurant_id=3, pizza_id=4),
            RestaurantPizza(price=16, restaurant_id=3, pizza_id=5),
        ]

        for rp in restaurant_pizzas:
            db.session.add(rp)

        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {len(restaurants)} restaurants")
        print(f"Created {len(pizzas)} pizzas")
        print(f"Created {len(restaurant_pizzas)} restaurant-pizza relationships")


if __name__ == '__main__':
    seed_data()