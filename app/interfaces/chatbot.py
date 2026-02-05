from app.services import utilities
from app.interfaces import cli

"""Este arquivo consta como interface de teste das funções dos services do projeto."""

def menu():

    try:
        login_or_register = int(input("""Olá, deseja entrar em uma conta ja existente ou realizar um cadastro?
0 - Entrar na minha conta
1 - Realizar cadastro
"""))
        
        if login_or_register == 0:
            logged_user = cli.login_validation()
        else:
            logged_user = cli.register()

        if logged_user:
            name_user = utilities.search_user_info(logged_user["email"])[1]
            print(f"Olá {name_user}, como posso te ajudar hoje?")
            while True:

                user_action  = int(input("""
1 - Fazer uma reserva
2 - Cancelar uma reserva
3 - Mostrar minhas reservas
4 - Mostrar destinos disponíveis
5 - Alterar meu cadastro
6 - Cancelar meu cadastro
0 - Sair
"""))

                if user_action == 1:
                    if not cli.action_show_active_destinations():
                        print("Não há destinos disponíveis no momento.")
                        continue

                    success = cli.action_create_reservation(logged_user["id"])

                    if success:
                        print("Reserva criada com sucesso!")
                    else:
                        print("Não foi possível criar a reserva.")

                elif user_action == 2:
                    success = cli.action_cancel_reservation(logged_user["id"])

                    if success:
                        print(f"Reserva de ID: {success} cancelada com sucesso.")
                    else:
                        print("Não foi possível deletar a reserva.")

                elif user_action == 3:
                    success = cli.action_show_reservations(logged_user["id"])

                    if success:
                        print("Aqui estão todas suas reservas.")
                    else:
                        print("Você não tem reservar para mostrar.")

                elif user_action == 4:
                    success = cli.action_show_active_destinations()

                    if success:
                        print("Estes são todos os destinos disponíveis no momento.")
                    else:
                        print("Não há destinos disponíveis no momento.")

                elif user_action == 5:
                    success = cli.action_change_user_info(logged_user["id"])

                    if success:
                        print("Dados alterados com sucesso")
                    else:
                        print("Não foi possível alterar seus dados.")

                elif user_action == 6:
                    success = cli.action_delete_user(logged_user["id"])

                    if success:
                        print("Cadastro excluído com sucesso.")
                        break
                    else:
                        print("Primeiro é necessário cancelar suas reservas.")

                elif user_action == 0:
                    print("Até mais!")
                    break

    except Exception:
        raise

if __name__ == "__main__":
    menu()