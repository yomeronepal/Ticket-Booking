from ..database import database as db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


class TimeTracker(db.Model):
    __tablename__ = "time_tracker"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(120), nullable=True)
    end_date = db.Column(db.String(120), nullable=True)
    task_description = db.Column(db.String(255), nullable=True)
    # Foreign key column referencing the 'id' column in the 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Establishing a relationship with the User model
    user = db.relationship("User", backref="time_trackers", lazy=True)
