from app.models.user import User
from app.utils.db import db

class AuthService:

    def register_user(self, name, email, password, role="roommate"):
        # check existing user
        existing = User.query.filter_by(email=email).first()
        if existing:
            return None

        # create new user
        user = User(
            name=name,
            email=email,
            role=role
        )

        # IMPORTANT: hash password
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        print("USER CREATED:", email)  # debug

        return user


    def login_user(self, email, password):
        print("LOGIN CHECK:", email)  # debug

        user = User.query.filter_by(email=email).first()

        if not user:
            print("NO USER FOUND")
            return None

        print("USER FOUND:", user.email)

        # check hashed password
        if user.check_password(password):
            print("PASSWORD MATCH")
            return user
        else:
            print("WRONG PASSWORD")

        return None