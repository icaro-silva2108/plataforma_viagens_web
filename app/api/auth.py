from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
import uuid

# Retorna a identidade do token
def get_access_token_identity():
    return get_jwt_identity()

# Retorna o refresh id(additional claim) do refresh_token
def get_refresh_id():
    return get_jwt().get("refresh_id")

# Retorna o access token criado
def send_access_token(user_id):
    return create_access_token(identity=str(user_id))

# Retorna o refresh token criado
def send_refresh_token(user_id):
    return create_refresh_token(identity=str(user_id), additional_claims={"refresh_id" : str(uuid.uuid4())})