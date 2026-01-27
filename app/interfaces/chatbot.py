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

                user_action  = int(input(f"""Olá {name_user}, como posso te ajudar hoje?
                                     1 - Fazer uma reserva
                                     2 - Cancelar uma reserva
                                     3 - Mostrar minhas reservas
                                     4 - Mostrar destinos disponíveis
                                     5 - Alterar meu cadastro
                                     6 - Cancelar meu cadastro
                                     0 - Sair"""))
                
                if user_action == 1:
                    success = cli.action_create_reservation(logged_user)

                    if success:
                        print("Reserva criada com sucesso!")
                    else:
                        print("Não foi possível criar a reserva.")
                
                elif user_action == 2:
                    success = cli.action_cancel_reservation(logged_user)
    except Exception as e:
        raise e