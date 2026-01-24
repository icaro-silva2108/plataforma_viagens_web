import bcrypt

def hash_password(password: str) -> str:# --> Faz o hasheamento da senha do usuário usando salt gerado pelo próprio bcrypt

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str) -> bool:# Verificação de hasheamento da senha, extraindo o salt para comparar hashes

    return bcrypt.checkpw(password.encode(), hashed_password.encode())