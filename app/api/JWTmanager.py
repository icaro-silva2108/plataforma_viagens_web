from flask_jwt_extended import JWTManager
from flask import jsonify
from app.services import utilities
import os
from dotenv import load_dotenv

load_dotenv()

jwt = JWTManager()

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):

    refresh_id = jwt_payload.get("refresh_id")

    return utilities.search_revoked_token(refresh_id)

@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):

    return jsonify({
        "success" : False,
        "message" : "Refresh Token Revogado."
        }), 401

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):

    return jsonify({
        "success" : False,
        "message" : "Token expirado."
        }), 401

@jwt.unauthorized_loader
def missing_auth_header(message):

    message = "Header de autorização não encontrado"

    return jsonify({
        "success" : False,
        "message" : message
    }), 401