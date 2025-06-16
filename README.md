# 🍕 Pizza Restaurant API

A RESTful API for managing pizza restaurants built with Flask, SQLAlchemy, and PostgreSQL following the MVC (
Model-View-Controller) architectural pattern.

## 🚀 Features

- **Restaurant Management**: Create, read, and delete restaurants
- **Pizza Catalog**: View available pizzas
- **Restaurant-Pizza Relationships**: Manage which pizzas are available at which restaurants with pricing
- **Data Validation**: Price validation (must be between $1-$30)
- **Cascading Deletes**: When a restaurant is deleted, all related restaurant-pizza relationships are automatically
  removed

## 🏗️ Project Structure

```
.
├── server/
│   ├── __init__.py
│   ├── app.py                # App setup and configuration
│   ├── config.py             # Database configuration
│   ├── models/               # 💾 Data Models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── restaurant.py     # Restaurant model
│   │   ├── pizza.py          # Pizza model
│   │   └── restaurant_pizza.py # Join table model
│   ├── controllers/          # 🎯 Route handlers (Controllers)
│   │   ├── __init__.py
│   │   ├── restaurant_controller.py
│   │   ├── pizza_controller.py
│   │   └── restaurant_pizza_controller.py
│   └── seed.py               # Database seeding script
├── migrations/               # Database migration files
├── challenge-1-pizzas.postman_collection.json
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pipenv (recommended) or pip

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd pizza-api-challenge

# Install dependencies using pipenv (recommended)
pipenv install flask flask_sqlalchemy flask_migrate psycopg2-binary
pipenv shell

# OR using pip
pip install -r requirements.txt
```

### 2. Database Setup

**Create PostgreSQL Database:**

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create database and user
CREATE DATABASE pizza_restaurant_db;
CREATE USER pizza_user WITH PASSWORD 'pizza_pass';
GRANT ALL PRIVILEGES ON DATABASE pizza_restaurant_db TO pizza_user;
\q
```

**Update Database Configuration:**
Edit `server/config.py` and update the database URI:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://pizza_user:pizza_pass@localhost/pizza_restaurant_db'
```

### 3. Initialize Database

```bash
# Set Flask app
export FLASK_APP=server/app.py

# Initialize migration repository
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration to database
flask db upgrade
```

### 4. Seed the Database

```bash
python server/seed.py
```

### 5. Run the Application

```bash
# Development mode
python server/app.py

# OR using Flask CLI
flask run
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Base URL

```
http://localhost:5000
```

### Endpoints

#### 🏪 Restaurants

##### GET /restaurants

Get all restaurants.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Dominion Pizza",
    "address": "Good Italian, Ngong Road, 4th Floor"
  },
  {
    "id": 2,
    "name": "Pizza Hut",
    "address": "Westgate Mall, Mwanzi Road"
  }
]
```

##### GET /restaurants/:id

Get a single restaurant with its pizzas.

**Success Response (200):**

```json
{
  "id": 1,
  "name": "Dominion Pizza",
  "address": "Good Italian, Ngong Road, 4th Floor",
  "pizzas": [
    {
      "id": 1,
      "name": "Cheese",
      "ingredients": "Dough, Tomato Sauce, Cheese"
    },
    {
      "id": 2,
      "name": "Pepperoni",
      "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
    }
  ]
}
```

**Error Response (404):**

```json
{
  "error": "Restaurant not found"
}
```

##### DELETE /restaurants/:id

Delete a restaurant and all related RestaurantPizzas.

**Success Response:** `204 No Content`

**Error Response (404):**

```json
{
  "error": "Restaurant not found"
}
```

#### 🍕 Pizzas

##### GET /pizzas

Get all pizzas.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Cheese",
    "ingredients": "Dough, Tomato Sauce, Cheese"
  },
  {
    "id": 2,
    "name": "Pepperoni",
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
  }
]
```

#### 🔗 Restaurant-Pizza Relationships

##### POST /restaurant_pizzas

Create a new RestaurantPizza relationship.

**Request Body:**

```json
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 1
}
```

**Success Response (201):**

```json
{
  "id": 4,
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 1,
  "pizza": {
    "id": 1,
    "name": "Cheese",
    "ingredients": "Dough, Tomato Sauce, Cheese"
  },
  "restaurant": {
    "id": 1,
    "name": "Dominion Pizza",
    "address": "Good Italian, Ngong Road, 4th Floor"
  }
}
```

**Error Response (400):**

```json
{
  "errors": [
    "Price must be between 1 and 30"
  ]
}
```

## ✅ Validation Rules

### RestaurantPizza

- **Price**: Must be between 1 and 30 (inclusive)
- **Restaurant ID**: Must reference an existing restaurant
- **Pizza ID**: Must reference an existing pizza

### Required Fields

- **RestaurantPizza**: `price`, `pizza_id`, `restaurant_id`

## 🧪 Testing with Postman

### Import Collection

1. Open Postman
2. Click **Import**
3. Upload `challenge-1-pizzas.postman_collection.json`
4. The collection will be imported with all test cases

### Environment Variables

Set the following variable in Postman:

- `base_url`: `http://localhost:5000`

### Test Cases Included

- ✅ Get all restaurants
- ✅ Get single restaurant (valid and invalid IDs)
- ✅ Delete restaurant (valid and invalid IDs)
- ✅ Get all pizzas
- ✅ Create restaurant-pizza relationship (valid)
- ✅ Create restaurant-pizza relationship (invalid price - too low)
- ✅ Create restaurant-pizza relationship (invalid price - too high)
- ✅ Create restaurant-pizza relationship (missing required fields)

## 🗄️ Database Schema

### Tables

#### restaurants

- `id` (Primary Key)
- `name` (String, Not Null)
- `address` (String, Not Null)

#### pizzas

- `id` (Primary Key)
- `name` (String, Not Null)
- `ingredients` (String, Not Null)

#### restaurant_pizzas

- `id` (Primary Key)
- `price` (Integer, Not Null, 1-30)
- `restaurant_id` (Foreign Key → restaurants.id)
- `pizza_id` (Foreign Key → pizzas.id)

### Relationships

- **Restaurant** has many **RestaurantPizzas** (one-to-many)
- **Pizza** has many **RestaurantPizzas** (one-to-many)
- **RestaurantPizza** belongs to **Restaurant** and **Pizza** (many-to-one)
- Cascading delete: When a Restaurant is deleted, all related RestaurantPizzas are automatically deleted

## 🚨 Error Handling

The API handles various error scenarios:

### 404 Errors

- Restaurant not found
- Pizza not found

### 400 Errors

- Invalid price (outside 1-30 range)
- Missing required fields
- Invalid data format

### Example Error Responses

**Validation Error:**

```json
{
  "errors": [
    "Price must be between 1 and 30"
  ]
}
```

**Not Found Error:**

```json
{
  "error": "Restaurant not found"
}
```

**Missing Fields Error:**

```json
{
  "errors": [
    "Missing required fields: price, pizza_id, restaurant_id"
  ]
}
```

## 🔄 Database Migration Commands

```bash
# Create a new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations to database
flask db upgrade

# Downgrade to previous migration (if needed)
flask db downgrade

# View migration history
flask db history
```

## 🌱 Sample Data

The seed script creates:

### Restaurants

1. **Dominion Pizza** - Good Italian, Ngong Road, 4th Floor
2. **Pizza Hut** - Westgate Mall, Mwanzi Road
3. **Kiki's Pizza** - Kilimani, Dennis Pritt Road

### Pizzas

1. **Cheese** - Dough, Tomato Sauce, Cheese
2. **Pepperoni** - Dough, Tomato Sauce, Cheese, Pepperoni
3. **California** - Dough, Sauce, Ricotta, Red peppers, Goat cheese, Italian sausage, Mushrooms
4. **Margherita** - Dough, Tomato Sauce, Fresh Mozzarella, Basil
5. **Hawaiian** - Dough, Tomato Sauce, Cheese, Ham, Pineapple

### Restaurant-Pizza Relationships

- Dominion Pizza: Cheese ($10), Pepperoni ($15)
- Pizza Hut: Cheese ($12), California ($18)
- Kiki's Pizza: Margherita ($14), Hawaiian ($16)

## 🚀 Deployment Considerations

### Environment Variables

For production, set these environment variables:

```bash
export DATABASE_URL=postgresql://username:password@hostname:port/database_name
export FLASK_ENV=production
```

### Production Configuration

Update `server/config.py` for production:

```python
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Troubleshooting

### Common Issues

**1. Database Connection Error**

- Ensure PostgreSQL is running
- Check database credentials in `config.py`
- Verify database exists

**2. Migration Errors**

- Delete `migrations/` folder and reinitialize
- Check for circular imports in models

**3. Import Errors**

- Ensure you're in the project root directory
- Check Python path and virtual environment

**4. Port Already in Use**

- Change port in `app.py`: `app.run(port=5001)`
- Kill existing process: `lsof -ti:5000 | xargs kill -9`

## 📞 API Testing Examples

### Using curl

**Get all restaurants:**

```bash
curl -X GET http://localhost:5000/restaurants
```

**Create restaurant-pizza relationship:**

```bash
curl -X POST http://localhost:5000/restaurant_pizzas \
  -H "Content-Type: application/json" \
  -d '{"price": 12, "pizza_id": 1, "restaurant_id": 2}'
```

**Delete a restaurant:**

```bash
curl -X DELETE http://localhost:5000/restaurants/1
```

## 📄 License

This project is created for educational purposes as part of a coding challenge.

---

**Happy Coding! 🍕**