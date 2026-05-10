from app.models.expense_split import ExpenseSplit
from app.utils.db import db

class SplitService:

    def equal_split(self, expense, user_ids):
        if not user_ids:
            return

        share = expense.amount / len(user_ids)

        for uid in user_ids:
            split = ExpenseSplit(
                expense_id=expense.expense_id,
                user_id=uid,
                share_amount=share,
                paid_status=False
            )
            db.session.add(split)

        db.session.commit()


    def custom_split(self, expense, split_map):
        total = sum(split_map.values())

        if total != expense.amount:
            return False

        for uid, amount in split_map.items():
            split = ExpenseSplit(
                expense_id=expense.expense_id,
                user_id=uid,
                share_amount=amount,
                paid_status=False
            )
            db.session.add(split)

        db.session.commit()
        return True