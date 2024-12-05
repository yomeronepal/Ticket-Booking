from ..database import database as db
from ..database.models import User, TimeTracker
from ..utils.password import Password
from ..database.tickets.models import TicketWaitList


class UserORM:
    def create_user(self, user_schema):
        user = User(
            name=user_schema.name,
            email=user_schema.email,
            age=user_schema.age,  # Hashing should be done here ideally
            password=Password().hash_password(user_schema.password),
            is_active=True,
            is_admin=user_schema.is_admin,
        )

        # Add to database session and commit
        db.session.add(user)
        db.session.commit()
        return user

    def create_wait_list(self, event_id, user_id, ticket_count):
        wait_list = TicketWaitList(
            event_id=event_id, user_id=user_id, ticket_count=ticket_count
        )
        db.session.add(wait_list)
        db.session.commit()
        return wait_list
