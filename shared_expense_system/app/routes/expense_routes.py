from flask import Blueprint, request, redirect, session, render_template
from app.services.expense_service import ExpenseService
from app.services.split_service import SplitService
from app.models.homespace import HomeMember

expense_bp = Blueprint("expense", __name__)

expense_service = ExpenseService()
split_service = SplitService()


# 🔵 ADD EXPENSE (UPDATED WITH USER TRACKING)
@expense_bp.route("/add_expense/<int:home_id>", methods=["GET", "POST"])
def add_expense(home_id):

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        description = request.form.get("description")

        # 🔥 get logged-in user
        user_id = session.get("user_id")

        # 🔥 pass user_id to service
        expense = expense_service.add_expense(
            home_id,
            amount,
            category,
            description,
            user_id
        )

        # 🔵 get all members for splitting
        members = HomeMember.query.filter_by(home_id=home_id).all()
        user_ids = [m.user_id for m in members]

        # 🔵 split equally
        split_service.equal_split(expense, user_ids)

        return redirect("/dashboard")

    return render_template("add_expense.html", home_id=home_id)