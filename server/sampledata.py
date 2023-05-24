"""Create Sample Data"""
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from server import create_server, db, bcrypt
from flask_migrate import upgrade,migrate,init,stamp
from models import User, Product

app = create_server()
app.app_context().push()
db.create_all()

def create_products():
# Create Test date for products
	products = [
		{'id': 0, 'name': 'Noodles', 'description': 'Noodles', 'costIncl': 10.00},
		{'id': 1, 'name': 'Meat Pie', 'description': 'Noodles', 'costIncl': 8.5},
		{'id': 2, 'name': 'Chicken Pie', 'description': 'Noodles', 'costIncl': 1.5},
		{'id': 3, 'name': 'Cheese Roll', 'description': 'Noodles', 'costIncl': 3.5},
		{'id': 4, 'name': 'Nuts', 'description': 'Noodles', 'costIncl': 6.5},
		{'id': 5, 'name': 'Soap', 'description': 'Noodles', 'costIncl': 8.5},
		{'id': 6, 'name': 'Pancakes', 'description': 'Noodles', 'costIncl': 10.00},
		{'id': 7, 'name': 'Bis', 'description': 'Noodles', 'costIncl': 7.5},
		{'id': 8, 'name': 'Pizza', 'description': 'Noodles', 'costIncl': 8.5},
		{'id': 9, 'name': 'Coke', 'description': 'Noodles', 'costIncl': 4.5}
		]

	for p in products:
		product = Product(name=p['name'], description=p['description'], costIncl=p['costIncl']) 
		db.session.add(product)
		db.session.commit()


# Create Admin user
def create_superuser():
	superuser = User(
		id=0, 
		username="admin", 
		fullname="Admin", 
		password=bcrypt.generate_password_hash("admin"), 
		level=0)		
	db.session.add(superuser)
	db.session.commit()


create_superuser()
create_products()