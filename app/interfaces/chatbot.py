from app.services import user_service, destination_service, reservation_service, utilities, security
from app.interfaces import cli

logged_user = None

def menu():

    try:
        login_or_register = int(input("""Olá, deseja entrar em uma conta ja existente ou realizar um cadastro?
                                  0 - Entrar na minha conta
                                  1 - Realizar cadastro"""))
        
        if login_or_register == 0:
            logged_user = cli.login_validation()
        else:
            logged_user = cli.register()

        if logged_user:
            
            name_user = utilities.get_name_user(logged_user)
            while True:

                user_action  = input(f"""Olá {name_user}, como posso te ajudar hoje?
                                     0 - Fazer uma reserva
                                     1 - Cancelar uma reserva
                                     2 - Mostrar minhas reservas
                                     3 - Mostrar destinos disponíveis
                                     4 - Alterar meu cadastro
                                     5 - Cancelar meu cadastro
                                     6 - Sair""")
                
    except Exception as e:
        raise e