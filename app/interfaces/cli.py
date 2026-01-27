from app.services import user_service, reservation_service, destination_service, utilities, security
from datetime import datetime, date

def birth_date_validation():

    try:

        while True:

            try:

                birth_date_str = input("Digite sua data de nascimento(dd/mm/aaaa):")# --> Recebe a data de nascimento do usuário
                birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()# --> Converte para objeto date

            except ValueError:# --> Caso não esteja no formato especificado, retorna para a inserção da data
                print("Formato de data inválido. Use (dd/mm/aaaa)")
                continue

            today = date.today()# --> Recebe a data atual
            age = today.year - birth_date.year# --> Recebe a diferença entre o ano atual e o ano de nascimento

            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1# --> Caso não tenha chagado o mês e dia de nascimento, reduz em 1 a idade para precisão do dado

            if age < 16:
                print("É preciso ter pelo menos 16 anos para criar uma conta.")
                continue
            break

        return birth_date# --> Retorna a data validada
    
    except Exception:
        raise

def register():

    try:
        name = input("Qual seu nome completo?").title()# --> Recebe nome de usuário

        while True:

            email = input("Digite seu email:")# --> Recebe email de usuário
            user_id = utilities.search_user_by_email(email)# --> Procura o id do usuário desse email no database
            if user_id:# --> Se já existir o id com o email cadastrado, impede a criação com o mesmo email
                print("Este email já está sendo usado. Tente outro email:")
                continue
            break

        while True:

            password = input("Crie uma senha que faça sentido para você:")# --> Recebe a senha do usuário
            password_confirm = input("Confirme sua senha:")# --> Faz a confirmação da senha
            if password != password_confirm:
                print("Não foi possível confirmar. Use a mesma senha do campo anterior.")
                continue
            break

        password_hash = security.hash_password(password)# --> Faz o hasheamento da senha antes de salvar no database

        birth_date = birth_date_validation()# --> Recebe a data de nascimento validada do usuário

        user_service.create_user(name, email, password_hash, birth_date)# --> Conclui o cadastro

        print("Cadastro realizado com sucesso!")
        user_id = utilities.search_user_by_email(email)
        return user_id# --> Retorna o id do usuário para realização de buscas nos services com um usuário específico

    except Exception:
        raise

def login_validation(email, password):

    try:

        while True:

            email = input("Digite seu email:")# --> Recebe o email
            password = input("Digite a senha do seu email:")# --> Recebe a senha

            user_id = user_service.login(email, password)# --> Faz a confirmação do login

            if not user_id:# --> Se encontrar o usuário e confirmar a senha, retorna o valor de seu id
                print("Email ou senha inválidos. Tente novamente.")
                continue
            
            break

        print("Login realizado com sucesso!")
        return user_id

    except Exception:
        raise

def action_create_reservation(user_id):

    try:

        while True:

            destination_id = int(input("Qual destino deseja reservar?"))

            if not utilities.search_destination(destination_id):
                print("Destino não disponível. Selecione outro válido")
                continue
            break

        while True:

            try:
                travel_date_str = input("Escolha a data da viagem(dd/mm/aaaa):")
                travel_date = datetime.strptime(travel_date_str, "%d/%m/%Y").date()

            except ValueError:
                print("Formato de data inválido. Use (dd/mm/aaaa)")
                continue

            if travel_date <= date.today():
                print("Escolha uma data futura. Datas de hoje e datas passadas não são aceitas")
                continue
            break

        reservation_confirm = reservation_service.create_reservation(user_id, destination_id, travel_date)
        return reservation_confirm

    except Exception:
        raise

def action_cancel_reservation(user_id):

    try:

        user_reservations = reservation_service.show_reservations(user_id)
        if not user_reservations:
            print("Você não tem reservas para cancelar.")
            return False

        print("Suas reservas:")
        for r in user_reservations:
            print(f"ID: {r[0]} | {r[1]} - {r[2]} | Data: {r[3]} | Status: {r[4]} | Preço: {r[5]}")

        while True:

            reservation_id = int(input("Digite o ID da reserva que quer cancelar(ou 0 para sair):"))
            
            if reservation_id == 0:
                print("Cancelamento abortado.")
                return False
            
            elif reservation_service.cancel_reservation(reservation_id, user_id):
                print(f"Reserva de ID: {reservation_id} cancelada com sucesso!")
                return True

            else:
                print("Reserva inválida. Escolha uma ID da lista.")
                

    except Exception:
        raise