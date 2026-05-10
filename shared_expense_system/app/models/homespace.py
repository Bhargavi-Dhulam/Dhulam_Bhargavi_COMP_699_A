from app.utils.db import db

class HomeSpace(db.Model):
    __tablename__ = "homes"

    home_id = db.Column(db.Integer, primary_key=True)

    home_name = db.Column(db.String(100), nullable=False)

    admin_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    created_date = db.Column(db.DateTime)



class HomeMember(db.Model):
    __tablename__ = "home_members"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    home_id = db.Column(db.Integer, db.ForeignKey("homes.home_id"))