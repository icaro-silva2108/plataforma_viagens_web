from flask import Flask
from app.api.public_routes import public_routes
from app.api.protected_routes import protected_routes
from app.api.JWTmanager import init_jwt

app = Flask(__name__, static_folder="static")
init_jwt(app)

app.register_blueprint(public_routes, url_prefix="/api")
app.register_blueprint(protected_routes, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)