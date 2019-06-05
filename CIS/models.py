from datetime import datetime
from CIS import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    runs = db.relationship('Run', backref='user', lazy=True)

    def __repr__(self):
        return "User('" + self.username + ", " + self.password + "')"


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(20), nullable=False)
    clusters = db.Column(db.Integer)
    compactness = db.Column(db.Float)
    separation = db.Column(db.Float)
    color = db.Column(db.String(1))
    date_ran = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    input_image = db.Column(db.String(20), nullable=False)
    output_image = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Run('" + self.algorithm + ", " + self.date_ran.strftime(
            '%d/%m/%y - %I:%M%p') + "')"
