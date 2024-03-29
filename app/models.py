import enum
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return Users.query.get(int(user_id))

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    stripe_secret_key = db.Column(db.String, default="")
    stripe_publishable_key = db.Column(db.String, default="")
    stripe_currency = db.Column(db.String, default="MDL")
    stripe_transaction_description = db.Column(db.String, default="Flask Order")

    aws_s3_bucket = db.Column(db.String, default="")
    aws_s3_key_id = db.Column(db.String, default="")
    aws_s3_key_secret = db.Column(db.String, default="")

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(60), nullable=False)

    firstname = db.Column(db.String)
    surname = db.Column(db.String)
    profile_picture = db.Column(db.String, nullable=False, default="default-user.png")

    def __repr__(self):
        return f"User({self.role} - {self.username}, {self.email} - {self.firstname} {self.surname})"

class Tables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=False)
    qrfilename = db.Column(db.String, nullable=False)
    qrurl = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"({self.id}) Table {self.number} with {self.seats} seats"

class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    #subcategories = db.relationship('Subcategories', backref='MenuSubCategory', lazy=True)
    dishes = db.relationship('MenuDish', backref='menu_category', lazy=True)
    filename = db.Column(db.String)
    thumbnail = db.Column(db.String)

    def __repr__(self):
        return f"{self.name}, {self.dishes}"

class MenuDish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    preparation_time = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    ingredients = db.Column(db.String)

    filename = db.Column(db.String)
    thumbnail = db.Column(db.String)
    category = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False)

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    all_data = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False, unique=True)
    created = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)

class OrderStatuses(enum.Enum):
    placed = "placed"
    active = "active"
    complete = "complete"

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    all_data = db.Column(db.String, nullable=False)
    # order details
    placed = db.Column(db.String, nullable=False)
    activated = db.Column(db.String)
    completed = db.Column(db.String)
    status = db.Column(db.Enum(OrderStatuses), default=OrderStatuses.placed, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    products = db.Column(db.String, nullable=False)
    preparation_time = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String)
    # payment details
    amount = db.Column(db.Integer, nullable=False)
    receipt = db.Column(db.String, nullable=False)
