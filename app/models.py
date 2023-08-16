from app import db
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(75), unique=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(25))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.password = generate_password_hash(kwargs.get('password'))

    def __repr__(self):
        return f"<Contact {self.id}|{self.first_name}>"
    
 