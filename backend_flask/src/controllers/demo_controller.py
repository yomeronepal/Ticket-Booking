from flask import g


def login():
    # here we will autehnticate user and
    # if true we will set cookie and return user details
    return "Login route"


def get_details():
    return {"hello": "Get details route"}


def test():
    return {"test": "test"}
