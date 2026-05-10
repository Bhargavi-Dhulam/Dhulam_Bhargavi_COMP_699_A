from flask import Blueprint, render_template, session, redirect
from app.models.expense import Expense
from app.models.user import User

report_bp = Blueprint("report", __name__)


@report_bp.route("/report/<int:home_id>")
def view_report(home_id):
    if "user_id" not in session:
        return redirect("/login")

    expenses = Expense.query.filter_by(home_id=home_id).all()

    #  attach user names
    expense_data = []
    for e in expenses:
        user = User.query.get(e.added_by)

        expense_data.append({
            "amount": e.amount,
            "category": e.category,
            "description": e.description,
            "added_by": user.name if user else "Unknown"
        })

    return render_template("report.html", expenses=expense_data)