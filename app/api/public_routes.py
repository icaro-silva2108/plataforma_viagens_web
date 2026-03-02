from flask import Blueprint, request, jsonify
from app.services import user_service, destination_service, utilities, security
from app.api.limiter import limiter
from app.api.auth import send_access_token, send_refresh_token

public_routes = Blueprint("public_routes", __name__)

@public_routes.route("/signup" , methods = ["POST"])
@limiter.limit("10 per minute")
def sign_up():

    data = request.get_json()
    if not data:
        return jsonify({
            "success" : False,
            "message" : "JSON inválido"
            }), 400

    name = data.get("name", "").strip().title()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    password_confirm = data.get("password_confirm", "").strip()
    birth_date_str = data.get("birth_date", "").strip()

    #Validação de todos os campos preenchidos
    if not all([name, email, password, password_confirm, birth_date_str]):
        return jsonify({
            "success" : False,
            "message" : "Campos vazios. Preencha todos os campos."
            }), 400

    #Email
    if not utilities.email_format_validation(email):
        return jsonify({
            "success" : False,
            "message" : "Formato de email inválido(email@email.com)."
            }), 400

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
    birth_date, error = utilities.birth_date_validation(birth_date_str)

    if not birth_date:

        if error == "format":
            return jsonify({
                "success" : False,
                "message" : "Formato de data inválido (dd/mm/aaaa)."
                }), 400

        if error == "age":
            return jsonify({
                "success" : False,
                "message" : "É preciso ter pelo menos 16 anos pra criar uma conta."
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

@public_routes.route("/signin", methods=["POST"])
@limiter.limit("10 per minute")
def sign_in():

    data = request.get_json()
    if not data:
        return jsonify({
            "success" : False,
            "message" : "JSON inválido"
            }), 400

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    # Verifica campos preenchidos
    if not all([email, password]):
        return jsonify({
            "success" : False,
            "message" : "Campos vazios. Preencha todos os campos."
            }), 400

    logged = user_service.login(email, password)

    # Erro de autenticação
    if not logged:
        return jsonify({
            "success" : False,
            "message" : "Email ou senha inválidos."
            }), 401

    # Cria tokens de usuário se autenticação for bem sucedida
    access_token = send_access_token(logged["id"])
    refresh_token = send_refresh_token(logged["id"])

    return jsonify({
        "success" : True,
        "user_id" : logged["id"],
        "name" : logged["name"],
        "email" : logged["email"],
        "access_token" : access_token,
        "refresh_token" : refresh_token
        }), 200

@public_routes.route("/destinations", methods=["GET"])
def show_homepage_destinations():

    destinations = destination_service.show_destinations()

    # Em caso de destinos vazios
    if not destinations:
        return jsonify({
            "success" : True,
            "destinations" : []
            }), 200

    results = []
    for d in destinations:
        results.append({
            "id" : d[0],
            "city" : d[1],
            "country" : d[2],
            "description" : d[3],
            "price" : float(d[4]),
            "img_url" : d[5]
        })

    return jsonify({
        "success" : True,
        "destinations" : results
        }), 200