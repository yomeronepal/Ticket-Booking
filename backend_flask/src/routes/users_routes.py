from flask import Blueprint, g

from ..controllers.users import (
    create_user,
    get_user,
    user_list,
    login,
    create_flows,
    flows_list,
    update_flows,
    flows_detail,
)
from ..controllers.demo_controller import get_details, test
from ..middlewares.protect import protect

user_routes = Blueprint("user", __name__)
user_routes.add_url_rule(
    "/create",
    view_func=lambda: create_user(),
    methods=["POST"],
    endpoint="user-create",
)
user_routes.add_url_rule(
    "/detail",
    view_func=lambda: protect(get_user)(),
    methods=["GET"],
    endpoint="get-user",
)

user_routes.add_url_rule(
    "/all",
    view_func=lambda: user_list(),
    methods=["GET"],
    endpoint="list-user",
)

user_routes.add_url_rule(
    "/login",
    view_func=lambda: login(),
    methods=["POST"],
    endpoint="login",
)

user_routes.add_url_rule(
    "/flows",
    view_func=lambda: protect(create_flows)(),
    methods=["POST"],
    endpoint="add-flows",
)

user_routes.add_url_rule(
    "/flows",
    view_func=lambda: protect(flows_list)(),
    methods=["GET"],
    endpoint="flows-list",
)

user_routes.add_url_rule(
    "/flows/<int:id>",
    view_func=lambda id: protect(update_flows)(id),
    methods=["PUT"],
    endpoint="update-flows",
)

user_routes.add_url_rule(
    "/flows/<int:id>",
    view_func=lambda id: protect(flows_detail)(id),
    methods=["GET"],
    endpoint="flows-detail",
)
