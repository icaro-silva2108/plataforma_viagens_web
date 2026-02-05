from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

jwt = JWTManager()

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt.init_app(app)