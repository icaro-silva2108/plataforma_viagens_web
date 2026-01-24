from app.services import user_service, reservation_service, destination_service, utilities, security

def register():

    try:
        name = input("Qual seu nome completo?").title()

        email = input("Digite seu email:")
        user_id = utilities.search_user_by_email(email)
        while user_id:
            email = input("Este email já está sendo usado. Tente outro email:")
            user_id = utilities.search_user_by_email(email)

        password = input("Crie uma senha que faça sentido para você:")
        password_confirm = input("Confirme sua senha:")
        while password != password_confirm:
            print("Não foi possível confirmar. Use a mesma senha do campo anterior.", end = "")
            password_confirm = input("Confirme sua senha:")

        password_hash = security.hash_password(password)

        birth_date = input("Digite sua data de nascimento(dd/mm/aaaa):")# --> lembrar de converter o tipo para data convencional sql

        user_service.create_user(name, email, password_hash, birth_date)

        print("Cadastro realizado com sucesso!", end = "")
        user_id = utilities.search_user_by_email(email)
        return user_id

    except Exception as e:
        raise e

def login_validation(email, password):

    try:

        while True:
            email = input("Digite seu email:")
            password = input("Digite a senha do seu email:")

            user_id = user_service.login(email, password)

            if user_id:
                print("Login realizado com sucesso!")
                break
            
            else:
                print("Email ou senha inválidos. Tente novamente.")
                return user_id

    except Exception as e:
        raise e
