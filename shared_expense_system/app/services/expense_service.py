from app.models.expense import Expense
from app.utils.db import db
from datetime import date


class ExpenseService:

    # 🔥 ADD EXPENSE WITH USER TRACKING
    def add_expense(self, home_id, amount, category, description, user_id):
        expense = Expense(
            home_id=home_id,
            amount=amount,
            category=category,
            description=description,
            date=date.today(),
            added_by=user_id   # 🔥 important
        )

        db.session.add(expense)
        db.session.commit()

        return expense


    # DELETE EXPENSE
    def delete_expense(self, expense_id):
        expense = Expense.query.get(expense_id)

        if expense:
            db.session.delete(expense)
            db.session.commit()

        return expense