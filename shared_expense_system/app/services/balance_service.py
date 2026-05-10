from app.models.expense_split import ExpenseSplit
from app.models.expense import Expense
from app.models.user import User


class BalanceService:

    def get_all_balances(self, home_id):
        splits = ExpenseSplit.query.join(Expense).filter(
            Expense.home_id == home_id
        ).all()

        balances = {}

        for split in splits:
            user = User.query.get(split.user_id)
            expense = Expense.query.get(split.expense_id)

            if not user or not expense:
                continue

            if user.user_id not in balances:
                balances[user.user_id] = {
                    "name": user.name,
                    "you_owe": 0,
                    "you_paid": 0
                }

            # If user added expense → they paid
            if expense.added_by == user.user_id:
                balances[user.user_id]["you_paid"] += expense.amount

            # If not paid yet → due
            if not split.paid_status:
                balances[user.user_id]["you_owe"] += split.share_amount

        return balances