# :pencil2: Descrição
Projeto pessoal de plataforma de viagens web que envolve funções como:  
- Criar cadastro  
- Acessar o cadastro  
- Cancelar cadastro  
- Alterar informações de cadastro  
- Criar reserva  
- Listar reservas  
- Cancelar reservas  
- Listar possíveis destinos

# :iphone: Tecnologias Utilizadas:
- Python  
- MySQL  
- Flask

## :books: Bibliotecas Utilizadas(Até o momento)

### :cd: Bibliotecas Python:
- os(Para variáveis de ambiente - Complementar dotenv)  
- datetime(Conversão para objeto data e verificação de datas válidas)  
- re(Validação de formato de email)  
- uuid(Geração de ID aleatório para blacklist de tokens)

### :dvd: Bibliotecas Externas
- mysql.connector(Integrar o Python ao banco MySQL)  
- dotenv(Ocultar dados sensíveis)  
- bcrypt(Hasheamento de senhas e validação para login)  
- flask(Para requests e reponses em json, blueprint de rotas)  
- flask-jwt-extended(Para autenticação com JWT e configuração do manager JWT)  
- flask_limiter(Rate limit de requisições das rotas)

# :bookmark_tabs: Estrutura do Projeto
- app/  
    - database/: Scripts SQL e conexão com o banco  
    - api/: Rotas, JWTmanager e rate limiter  
    - interfaces/: Testes  
    - services/: Regras de negócio, utilities e security(para hasheamento de senhas)

# :chart_with_upwards_trend: Objetivo do Projeto
O objetivo é consolidar na prática conhecimentos de programação e banco de dados por meio do desenvolvimento de um sistema próximo
de uma situação real e desafiadora para meu começo. A aplicação ajuda a entender e executar fundamentos de SQL como CRUD básico, integração MySQL - Python.
Além disso, o projeto serve como base de evolução para atribuição de API utilizando Flask, possibilitando a criação de uma interface Web e 
aprofundando na comunicação entre camadas e manipulação de dados em um contexto mais próximo ao ambiente profissional.
Trata-se de um projeto visando o desenvolvimento pessoal e a possibilidade de dar mais um passo à frente de conseguir
consolidar a minha formação como desenvolvedor.

# :hourglass: Próximos Passos
- Novos testes no postman.  
- Testes automatizados.  
- Melhorar documentação.  
- Posteriormente, foco em desenvolvimento frontend.


# :computer: Como Rodar o Projeto Localmente

## :page_facing_up: 1. Requisitos iniciais:

- Tenha instalado o Python com versão maior ou igual a 3.9+(Recomendação: 3.11.9 - Usada para o desenvolvimento)  
- Escolha uma pasta que deseja alocar o projeto(opcional).
- Tenha o MySQL instalado e em execução.

## :inbox_tray: 2. Clone o Repositório:

- Abra o Git Bash em uma pasta de sua preferência.  
- Dentro do terminal Git use:  
```bash
git clone https://github.com/icaro-silva2108/plataforma_viagens_web.git
```
- Acesse a pasta criada:  
```console
cd plataforma_viagens_web
```

## :wrench: 3. Configuração de Ambiente:

- Dentro da pasta do projeto inicie o ambiente virtual através do terminal:  
```console
python -m venv venv
```  
- Ative o ambiente virtual com:  
```console
venv\Scripts\Activate
```  
- Obs: Certifique-se de que aparece "(venv)" antes do caminho no terminal.

## :file_folder: 4. Instalar Dependências(Libs):

- Use o arquivo requirements.txt para instalar as Libs externas:  
```console
pip install -r requirements.txt
```

## :game_die: 5. Configurar Database:

- Usando o MySQL, crie um Schema que será conectado ao projeto.
```sql
CREATE DATABASE plataforma_viagens;
```
- Use os scripts para criar as tabelas em localizados em:  
app/database/tables.sql  
app/database/destinations_seed.sql  
app/database/token_blacklist.sql

## :recycle: 6. Configure o .env:

- Adicione um arquivo .env no projeto.  
- Para definir as variáveis de ambiente necessárias, use o arquivo .env.example do repositório como referência.

## :microscope: 7. Executar e Testar a API:

- Com o ambiente virtual ativado, execute:  
```console
python -m main
```
- A rota do servidor deve aparecer em algo como:  
```console
Running on http://127.0.0.1:5000
```

### Para testar você pode usar as seguintes ferramentas:

- Postman
- Insomnia
- Thunder Client(VS Code)

Exemplo(Rota pública, não precisa de autenticação):
```console
GET http://127.0.0.1:5000/destinations
```