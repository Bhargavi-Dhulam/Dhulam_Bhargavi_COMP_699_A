from flask import Blueprint, render_template, session, redirect
from app.models.expense_split import ExpenseSplit
from app.models.expense import Expense

reminder_bp = Blueprint("reminder", __name__)


@reminder_bp.route("/reminders")
def reminders():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")

    # get unpaid expense shares for this user
    splits = ExpenseSplit.query.filter_by(
        user_id=user_id,
        paid_status=False
    ).all()

    reminder_data = []

    for s in splits:
        expense = Expense.query.get(s.expense_id)

        if not expense:
            continue

        reminder_data.append({
            "amount": s.share_amount,
            "category": expense.category,
            "description": expense.description
        })

    return render_template("reminders.html", reminders=reminder_data)