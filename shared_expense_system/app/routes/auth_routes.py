from flask import Blueprint, render_template, request, redirect, session
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

auth_service = AuthService()


# Root route
@auth_bp.route("/")
def home():
    print("HOME ROUTE HIT")

    if "user_id" in session:
        print("USER IN SESSION → DASHBOARD")
        return redirect("/dashboard")

    print("NO SESSION → LOGIN")
    return redirect("/login")


# Register
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        print("REGISTER TRY:", name, email)

        user = auth_service.register_user(name, email, password)

        if user:
            print("REGISTER SUCCESS")
            return redirect("/login")

        print("REGISTER FAILED - USER EXISTS")
        return render_template("register.html", error="User already exists")

    return render_template("register.html")


# Login (FULL DEBUG)
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        print("------ LOGIN REQUEST START ------")

        email = request.form.get("email")
        password = request.form.get("password")

        print("EMAIL:", email)
        print("PASSWORD:", password)

        user = auth_service.login_user(email, password)

        print("USER OBJECT:", user)

        if user:
            print("LOGIN SUCCESS")

            session["user_id"] = user.user_id
            session["role"] = user.role

            print("SESSION SET:", session)

            return redirect("/dashboard")

        print("LOGIN FAILED → STAY ON LOGIN PAGE")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


# Logout
@auth_bp.route("/logout")
def logout():
    print("LOGOUT USER:", session.get("user_id"))

    session.clear()

    return redirect("/login")