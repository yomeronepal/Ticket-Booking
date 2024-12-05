from flask import jsonify, request
from flask import Flask, g

from ..orm.user import UserORM
from ..utils.password import Password

from ..utils.token import generate_token
from ..database.models import User, TimeTracker
from ..pydantic.schemas import (
    UserRequestSchema,
    UserResponseSchema,
    GenericListSchema,
    LoginSchema,
    TimeTrackerRequestSchema,
    TimeTrackerResponseSchema,
)
from ..database import database
from pydantic import ValidationError
import json
from ..utils.pagination import get_paginated_response
from datetime import datetime


def format_pydantic_errors(errors):
    formatted_errors = []
    for error in errors:
        formatted_errors.append(
            {
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )
    return formatted_errors


def create_user():
    # try:
    # Assuming data is coming from request body
    data = g.request_json_body

    # Validate and create user schema
    user_schema = UserRequestSchema(**data)
    # Create user object
    user = UserORM().create_user(user_schema)

    # Return the newly created user as a response
    return jsonify(UserResponseSchema.from_orm(user).dict()), 201


def get_user():
    user = g.user
    return jsonify(UserResponseSchema.from_orm(user).dict())


def user_list():
    users = User.query.filter(User.name == "Rojesh")
    schema = GenericListSchema[UserResponseSchema]
    response = get_paginated_response(users, request, schema)

    # Return the serialized data with Flask's jsonify
    return response


def login():
    data = g.request_json_body

    # Validate and create user schema
    user_schema = LoginSchema(**data)
    user = User.query.filter(User.email == user_schema.email).first()
    token = None
    if user:
        if Password().check_password(user.password, user_schema.password):
            token = generate_token(user.id)
        else:
            raise ValueError("Email or Password is incorrect")
    else:
        raise ValueError("User not found")
    return jsonify({"token": token, "success": True}, 200)


def create_flows():
    data = g.request_json_body

    # Validate and create user schema
    time_tracker_schema = TimeTrackerRequestSchema(**data)
    user = g.user
    # Create user object
    time_tracker = TimeTracker(
        start_date=time_tracker_schema.start_date,
        end_date=time_tracker_schema.end_date,
        task_description=time_tracker_schema.task_description,  # Hashing should be done here ideally
        user=user,
    )

    # Add to database session and commit
    g.database.session.add(time_tracker)
    g.database.session.commit()

    # Return the newly created user as a response
    return jsonify(TimeTrackerResponseSchema.from_orm(time_tracker).dict()), 201


def flows_list():
    user = g.user
    query = TimeTracker.query.filter(TimeTracker.user == user)
    schema = GenericListSchema[TimeTrackerResponseSchema]
    response = get_paginated_response(query, request, schema)

    # Return the serialized data with Flask's jsonify
    return response


def update_flows(id):
    user = g.user
    query = TimeTracker.query.filter(TimeTracker.id == id).first()
    if not query:
        raise ValueError("Object not found")
    if query.user != user:
        raise ValueError("Time Tracker doesn't belong to user")
    query.end_date = datetime.now()
    g.database.session.commit()
    return jsonify(TimeTrackerResponseSchema.from_orm(query).dict()), 201


def flows_detail(id):
    user = g.user
    time_tracker = TimeTracker.query.filter(TimeTracker.id == id).first()

    # Return the serialized data with Flask's jsonify
    return jsonify(TimeTrackerResponseSchema.from_orm(time_tracker).dict()), 200
