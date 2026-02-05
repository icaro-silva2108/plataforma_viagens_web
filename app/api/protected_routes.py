from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import user_service, reservation_service, destination_service, utilities

protected_routes = Blueprint("protected_routes", __name__)

@protected_routes.route("/me", methods=["GET"])
@jwt_required()
def myprofile():

    # ID usuário
    user_id = get_jwt_identity()

    # Query de usuário
    user = utilities.search_user_by_id(user_id)

    if not user:
        return jsonify({
            "success" : False,
            "message" : "Usuário não encontrado."
            }), 404

    # Dados usuário
    name, email, birth_date = user

    return jsonify({
        "success" : True,
        "user" : {
            "id" : user_id,
            "name" : name,
            "email" : email,
            "birth_date" : birth_date
            }
        }), 200

@protected_routes.route("/reservations", methods=["POST"])
@jwt_required()
def create_reservation():

    # ID usuário
    user_id = get_jwt_identity()

    # JSON
    data = request.get_json()
    if not data:
        return jsonify({
            "success" : False,
            "message" : "JSON inválido"
            }), 400

    # ID destino
    destination_id = data.get("destination_id")

    if not utilities.search_destination(destination_id):
        return jsonify({
            "success" : False,
            "message" : "Destino não disponível ou não encontrado."
            }), 404

    # Data da viagem
    travel_date_str = data.get("travel_date")
    travel_date = utilities.travel_date_validation(travel_date_str)

    if not travel_date:
        return jsonify({
            "success" : False,
            "message" : "Data inválida. São aceitas somente datas posteriores à data de hoje."
            }), 400

    reservation_confirm = reservation_service.create_reservation(user_id, destination_id, travel_date)

    if not reservation_confirm:
        return jsonify({
            "success" : False,
            "message" : "Não foi possível criar a reserva."
        }), 500

    return jsonify({
        "success" : True,
        "reservation_id" : reservation_confirm
        }), 201

@protected_routes.route("/reservations", methods=["GET"])
@jwt_required()
def show_user_reservations():

    # ID usuário
    user_id = get_jwt_identity()

    # Reservas do usuário
    reservations = reservation_service.show_reservations(user_id)

    if not reservations:
        return jsonify({
            "success" : True,
            "user_reservations" : []
            }), 200

    results = []

    for r in reservations:
        results.append({
            "id" : r[0],
            "city" : r[1],
            "country" : r[2],
            "travel_date" : r[3],
            "status" : r[4],
            "price" : r[5],
            "img_url" : r[6],
        })

    return jsonify({
        "success" : True,
        "user_reservations" : results
        }), 200

@protected_routes.route("/reservations/<int:res_id>", methods=["DELETE"])
@jwt_required()
def cancel_reservation(res_id):

    # ID usuário
    user_id = get_jwt_identity()

    cancel_confirm = reservation_service.cancel_reservation(res_id, user_id)

    if not cancel_confirm:
        return jsonify({
            "success" : False,
            "message" : "Reserva não encontrada ou não pertence ao usuário."
            }), 404

    return jsonify({
        "success" : True,
        "message" : f"Reserva de ID: {res_id} cancelada com sucesso.",
        "canceled_res_id" : res_id
        }), 200