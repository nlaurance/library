from flask import Blueprint, current_app
from flask_restful import Api

from library.extensions import apispec
from library.api.resources import UserResource, UserList
from library.api.resources import BookRequestResource, BookRequestList
from library.api.resources.user import UserSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>")
api.add_resource(UserList, "/users")
api.add_resource(BookRequestResource, "/request/<int:request_id>")
api.add_resource(BookRequestList, "/request")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
