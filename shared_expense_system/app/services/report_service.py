from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

class ReportService:

    def get_home_expenses(self, home_id):
        return Expense.query.filter_by(home_id=home_id).all()


    def get_user_summary(self, home_id):
        splits = ExpenseSplit.query.join(Expense).filter(
            Expense.home_id == home_id
        ).all()

        summary = {}

        for split in splits:
            uid = split.user_id
            summary[uid] = summary.get(uid, 0) + split.share_amount

        return summary