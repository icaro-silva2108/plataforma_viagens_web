from flask import Blueprint, request, jsonify
from app.services import user_service, utilities, security
from flask_jwt_extended import create_access_token

public_routes = Blueprint("public_routes", __name__)

@public_routes.route("/register" , methods = ["POST"])
def register():

    data = request.get_json()
    if not data:
        return jsonify({
            "success" : False,
            "message" : "JSON inválido"
            }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    password_confirm = data.get("password_confirm")
    birth_date_str = data.get("birth_date")

    #Validação de todos os campos preenchidos
    if not all([name, email, password, password_confirm, birth_date_str]):
        return jsonify({
            "success" : False,
            "message" : "Campos vazios. Preencha todos os campos."
            }), 400

    #Email
    if utilities.search_user_info(email):
        return jsonify({
            "success" : False,
            "message" : "Este email já está sendo utilizado. Tente outro email."
            }), 409

    #Senha
    if password != password_confirm:
        return jsonify({
            "success" : False,
            "message" : "A senha e sua confirmação devem ser iguais."
            }), 400

    password_hash = security.hash_password(password)

    #Data de nascimento
    birth_date = utilities.birth_date_validation(birth_date_str)

    if not birth_date:
        return jsonify({
            "success" : False,
            "message" : "É preciso ter pelo menos 16 anos para criar uma conta"
            }), 400

    #Criação do usuário
    user_id = user_service.create_user(
        name,
        email,
        password_hash,
        birth_date
        )

    if not user_id:
        return jsonify({
            "success" : False,
            "message" : "Não foi possível criar o usuário."
            }), 500

    return jsonify({
        "success" : True,
        "user_id" : user_id,
        "name" : name,
        "email" : email
        }), 201

@public_routes.route("/login", methods=["POST"])
def login():

    data = request.get_json()
    if not data:
        return jsonify({
            "success" : False,
            "message" : "JSON inválido"
            }), 400

    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({
            "success" : False,
            "message" : "Campos vazios. Preencha todos os campos."
            }), 400

    logged = user_service.login(email, password)

    if not logged:
        return jsonify({
            "success" : False,
            "message" : "Email ou senha inválidos."
        }), 401

    user_token = create_access_token(identity=logged["id"])

    return jsonify({
        "success" : True,
        "user_id" : logged["id"],
        "name" : logged["name"],
        "email" : logged["email"],
        "token" : user_token
    }), 200