from flask import Blueprint, g
from ..controllers.demo_controller import get_details, test
from ..middlewares.protect import protect

demo_routers = Blueprint("api", __name__)


demo_routers.add_url_rule(
    "/all",
    view_func=lambda: protect(get_details)(),
    methods=["GET"],
    endpoint="get_all_details",
)
demo_routers.add_url_rule(
    "/test", view_func=lambda: test(), methods=["GET"], endpoint="test"
)
