from app.utils.db import db

class Expense(db.Model):
    __tablename__ = "expenses"

    expense_id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    description = db.Column(db.String(200))

    date = db.Column(db.Date)

    #  Home reference
    home_id = db.Column(db.Integer, db.ForeignKey("homes.home_id"))

    # NEW: Who added this expense
    added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    # Update expense
    def update_expense(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        db.session.commit()

    # Delete expense
    def delete_expense(self):
        db.session.delete(self)
        db.session.commit()