from app.utils.db import db

class ExpenseSplit(db.Model):
    __tablename__ = "expense_splits"

    split_id = db.Column(db.Integer, primary_key=True)

    expense_id = db.Column(db.Integer, db.ForeignKey("expenses.expense_id"))

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    share_amount = db.Column(db.Float, nullable=False)

    paid_status = db.Column(db.Boolean, default=False)

    def mark_paid(self):
        self.paid_status = True
        db.session.commit()