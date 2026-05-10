from app.models.reminder import Reminder
from app.models.expense_split import ExpenseSplit
from app.utils.db import db
from datetime import date

class ReminderService:

    def generate_reminders(self, user_id):
        splits = ExpenseSplit.query.filter_by(
            user_id=user_id,
            paid_status=False
        ).all()

        for split in splits:
            reminder = Reminder(
                user_id=user_id,
                send_date=date.today(),
                status="pending"
            )
            db.session.add(reminder)

        db.session.commit()


    def get_user_reminders(self, user_id):
        return Reminder.query.filter_by(user_id=user_id).all()