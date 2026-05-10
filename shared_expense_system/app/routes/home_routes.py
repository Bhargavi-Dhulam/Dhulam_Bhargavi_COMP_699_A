from flask import Blueprint, render_template, request, redirect, session, flash
from app.utils.db import db
from app.models.homespace import HomeSpace, HomeMember
from app.models.user import User
from app.services.balance_service import BalanceService

home_bp = Blueprint("home", __name__)

# 🔥 Initialize balance service
balance_service = BalanceService()


# 🔵 DASHBOARD (WITH ROOMMATES)
@home_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Get all homes of this user
    memberships = HomeMember.query.filter_by(user_id=user_id).all()
    home_ids = [m.home_id for m in memberships]

    homes = HomeSpace.query.filter(HomeSpace.home_id.in_(home_ids)).all()

    # Attach roommates
    home_data = []

    for home in homes:
        members = HomeMember.query.filter_by(home_id=home.home_id).all()

        users = []
        for m in members:
            user = User.query.get(m.user_id)
            if user:
                users.append(user)

        home_data.append({
            "home": home,
            "members": users
        })

    return render_template("dashboard.html", home_data=home_data)


# 🔵 CREATE HOME
@home_bp.route("/create_home", methods=["GET", "POST"])
def create_home():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        home_name = request.form.get("home_name")
        admin_id = session.get("user_id")

        # Create home
        home = HomeSpace(home_name=home_name, admin_id=admin_id)
        db.session.add(home)
        db.session.commit()

        # Add admin as member
        member = HomeMember(user_id=admin_id, home_id=home.home_id)
        db.session.add(member)
        db.session.commit()

        flash("Home created successfully!", "success")

        return redirect("/dashboard")

    return render_template("create_home.html")


# 🔵 JOIN HOME (WITH VALIDATION)
@home_bp.route("/join_home", methods=["GET", "POST"])
def join_home():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        # Validate input
        try:
            home_id = int(request.form.get("home_id"))
        except:
            flash("Invalid Home ID format", "error")
            return redirect("/join_home")

        user_id = session.get("user_id")

        # Check if home exists
        home = HomeSpace.query.get(home_id)
        if not home:
            flash("Home ID not found. Please check and try again.", "error")
            return redirect("/join_home")

        # Prevent duplicate join
        existing = HomeMember.query.filter_by(
            user_id=user_id,
            home_id=home_id
        ).first()

        if existing:
            flash("You are already part of this home.", "warning")
            return redirect("/dashboard")

        # Add user to home
        member = HomeMember(user_id=user_id, home_id=home_id)
        db.session.add(member)
        db.session.commit()

        flash("Successfully joined the home!", "success")

        return redirect("/dashboard")

    return render_template("join_home.html")


# 🔵 VIEW BALANCES (NEW - FINAL)
@home_bp.route("/balances/<int:home_id>")
def view_balances(home_id):
    if "user_id" not in session:
        return redirect("/login")

    balances = balance_service.get_all_balances(home_id)

    return render_template("balances.html", balances=balances)