from flask_jwt_extended import JWTManager
from app.services import utilities
import os
from dotenv import load_dotenv

load_dotenv()

jwt = JWTManager()

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)

@jwt.token_in_blocklist_loader
def check_revoked_token(jwt_header, jwt_payload):

    resfresh_id = jwt_payload.get("refresh_id")

    if not resfresh_id:
        return False
    
    return utilities.search_revoked_token(resfresh_id)