from app.utils.db import db

class Reminder(db.Model):
    __tablename__ = "reminders"

    reminder_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    send_date = db.Column(db.Date)

    status = db.Column(db.String(20))  # pending or sent

    def mark_sent(self):
        self.status = "sent"
        db.session.commit()