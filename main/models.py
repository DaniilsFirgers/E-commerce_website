from main import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ads = db.relationship('Ad', backref='seller', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.phone_number})"


class Ad(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500), default="No description")
    price = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(10), nullable=False)
    image = db.Column(db.String(50), default="default.jpg", nullable=False)
    characteristics = db.Column(db.String(200), default="No Info", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Ad({self.brand}, {self.category}, {self.characteristics}, {self.price}, {self.condition}, {self.user_id})"
# Run once to create the database
db.create_all()
