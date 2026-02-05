from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import user_service, reservation_service, destination_service, utilities

protected_routes = Blueprint("protected_routes", __name__)

@protected_routes.route("/me", methods=["GET"])
@jwt_required()
def myprofile():

    user_id = get_jwt_identity()

    return jsonify({
        "success" : True,
        "user_id" : user_id
        })