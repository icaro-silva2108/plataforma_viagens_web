from app.services import user_service, reservation_service, destination_service, utilities, security

"""Este arquivo consta como interface de teste das funções dos services do projeto."""

def register():

    try:
        name = input("Qual seu nome completo?").title()# --> Recebe nome de usuário

        while True:

            email = input("Digite seu email: ")# --> Recebe email de usuário
            user = utilities.search_user_info(email)# --> Procura o id do usuário desse email no database
            if user:# --> Se já existir o id com o email cadastrado, impede a criação com o mesmo email
                print("Este email já está sendo usado. Tente outro email: ")
                continue
            break

        while True:

            password = input("Crie uma senha que faça sentido para você: ")# --> Recebe a senha do usuário
            password_confirm = input("Confirme sua senha: ")# --> Faz a confirmação da senha
            if password != password_confirm:
                print("Não foi possível confirmar. Use a mesma senha do campo anterior.")
                continue
            break

        password_hash = security.hash_password(password)# --> Faz o hasheamento da senha antes de salvar no database

        while True:

            birth_date_str = input("Digite sua data de nascimento(aaaa-mm-dd): ")
            birth_date = utilities.birth_date_validation(birth_date_str)
            if not birth_date: # --> Recebe a data de nascimento validada do usuário
                print("É preciso ter pelo menos 16 anos para criar uma conta.")
                continue
            break

        user_id = user_service.create_user(name, email, password_hash, birth_date)# --> Conclui o cadastro

        print("Cadastro realizado com sucesso!")
        return {"id" : user_id, "email" : email}# --> Retorna o id do usuário para realização de buscas nos services com um usuário específico

    except Exception:
        raise

def login_validation():

    try:

        while True:

            email = input("Digite seu email: ")# --> Recebe o email
            password = input("Digite a senha da sua conta: ")# --> Recebe a senha

            user_info = utilities.search_user_info(email)# --> Faz a confirmação do login
            user_id, _, _ = user_info

            if not user_service.login(email, password):# --> Se encontrar o usuário e confirmar a senha, retorna o valor de seu id
                print("Email ou senha inválidos. Tente novamente.")
                continue

            break

        print("Login realizado com sucesso!")
        return {"id" : user_id, "email" : email}

    except Exception:
        raise

def action_create_reservation(user_id):

    try:

        while True:

            destination_id = int(input("Qual destino deseja reservar? "))# --> Recebe o id do destino para criar uma reserva

            if not utilities.search_destination(destination_id):
                print("Destino não disponível. Selecione outro válido")# --> Se o id for de um destino inativo ou que não existe, retorna para a escolha do id
                continue
            break

        while True:

            travel_date_str = input("Escolha a data da viagem(aaaa-mm-dd): ")# --> Recebe a data que será feita a viagem
            travel_date = utilities.travel_date_validation(travel_date_str)
            if not travel_date:
                print("Escolha uma data futura. Data de hoje e datas passadas não são aceitas.")
                continue
            break

        reservation_confirm = reservation_service.create_reservation(user_id, destination_id, travel_date)# --> Cria a reserva
        return reservation_confirm

    except Exception:
        raise

def action_cancel_reservation(user_id):

    try:

        user_reservations = reservation_service.show_reservations(user_id)# --> Recebe as reservas do usuário
        if not user_reservations:
            print("Você não tem reservas para cancelar.")# --> Se não tiver reservas, comunica a ausência e retorna para o menu
            return False

        print("Suas reservas:")
        for r in user_reservations:
            print(f"ID: {r[0]} | {r[1]} - {r[2]} | Data: {r[3]} | Status: {r[4]} | Preço: {r[5]}")# --> Lista as reservas para o usuário escolher qual deseja cancelar

        while True:

            reservation_id = int(input("Digite o ID da reserva que quer cancelar(ou 0 para sair): "))# --> Recebe o id da reserva que deseja cancelar ou opção 0 para abortar o cancelamento

            if reservation_id == 0:# --> Aborta o cancelamento e retorna ao menu
                print("Cancelamento abortado.")
                return False

            elif reservation_service.cancel_reservation(reservation_id, user_id):# --> Cancela a reserva
                return reservation_id

            else:
                print("Reserva inválida. Escolha uma ID da lista.")# --> Se id de reserva for inválido, comunica que não foi possível cancelar

    except Exception:
        raise

def action_show_reservations(user_id):

    try:

        user_reservations = reservation_service.show_reservations(user_id)# --> Recebe as reservas do usuário
        if not user_reservations:# --> Se o usuário não tiver reservas, comunica a ausência
            return False

        print("Suas reservas:")
        for r in user_reservations:
            print(f"ID: {r[0]} | {r[1]} - {r[2]} | Data: {r[3]} | Status: {r[4]} | Preço: {r[5]}")# --> Lista as reservas do usuário

        return True

    except Exception:
        raise

def action_show_active_destinations():

    try:

        active_destinations = destination_service.show_destinations()# --> Recebe os destinos ativos para realização de reservas
        if not active_destinations:# --> Se não houver destinos disponíveis, comunica a falta de destinos
            return False

        for d in active_destinations:
            print(f"{d[0]} | {d[1]} - {d[2]} | Preço: {d[4]} | Descrição: {d[3]}")# --> Mostra os destinos ativos

        return True

    except Exception:
        raise

def action_change_user_info(user_id):

    try:

        data = {}# --> Dicionário de dados que será enviado para a função change_user_info(user_id, info: dict)

        keys_to_change=input("""Dados possíveis: Nome, email e senha
Digite os dados que deseja alterar:
""")# --> Recebe quais dados serão alterados
        values_to_insert=input("""Na mesma ordem de dos dados que deseja alterar, digite os novos valores:
""")# --> Recebe quais valores substituirão os dados antigos

        keys_list = keys_to_change.split()# --> Cria uma lista dos dados que serão alterados
        values_list = values_to_insert.split()# --> Cria uma lista dos valores que substituirão dados antigos

        for k, v in zip(keys_list, values_list):# --> Atualiza o dict data inserindo pares de {dado a ser alterado : valor desse dado}
            if k == "nome":# --> Traduz a chaves nome para o formato presente na função change_user_info(user_id, info: dict)
                data.update({"name" : v.title()})
            elif k == "senha":# --> Traduz a chave senha para o formato presente na função change_user_info(user_id, info: dict) e faz o hasheamento da senha nova
                data.update({"password_hash" : security.hash_password(v)})
            elif k == "email":# --> Reconhece a chave email e insere o par no dict data
                data.update({"email" : v})

        if user_service.change_user_info(user_id, data):# --> Se conseguir fazer a alteração, retorna o sucesso da transação
            return True
        else:# --> Caso contrário, retorna falha
            return False

    except Exception:
        raise

def action_delete_user(user_id):

    try:

        confirm=int(input("""Certeza que deseja excluír seu cadastro?
0 - Sim
1 - Não
"""))# --> Confirmação da certeza de exclusão do cadastro

        if confirm == 0:# --> Se confirmar tenta deletar
            if user_service.delete_user(user_id):
                return True# --> Se a exclusão for concluída, confirma que foi deletado
            else:
                return False# --> Se o usuário tiver reservas, comunica que é necessário cancelar as reservas primeiro

        else:
            return False# --> Se o usuário não confirmar, retorna para o menu

    except Exception:
        raise