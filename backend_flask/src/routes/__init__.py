from flask import Blueprint, g, Request, jsonify
from .demo_routes import demo_routers
from .users_routes import user_routes
from .tickets_routes import ticket_routes
from .stripe_webhooks_routes import stripe_webhooks_routers

api_routes = Blueprint("api", __name__)


@api_routes.route("/demo")
def demo():
    return {"message": "Hello World"}


@api_routes.route("/db-status")
def db_status():
    db_name = g.database.engine.url.database
    # Logic to check database status
    return {
        "status": "success",
        "message": f"Database connected successfully to {db_name}",
    }


# define all your sub-routes here
# -------------------------------
api_routes.register_blueprint(demo_routers, url_prefix="/demo")
api_routes.register_blueprint(user_routes, url_prefix="/user")
api_routes.register_blueprint(ticket_routes, url_prefix="/ticket")
api_routes.register_blueprint(stripe_webhooks_routers, url_prefix="/webhooks")
# -------------------------------

# all the routes other than defined above will throw 404 error


@api_routes.errorhandler(404)
def page_not_found(e):
    return {"message": "Page not found"}, 404
