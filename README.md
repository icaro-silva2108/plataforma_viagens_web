# Descrição
Projeto pessoal de chatbot de atendimento para viagens que envolve funções como:<br>
• Criar cadastro<br>
• Acessar o cadastro<br>
• Cancelar cadastro<br>
• Alterar informações de cadastro<br>
• Criar reserva<br>
• Listar reservas<br>
• Cancelar reservas<br>
• Listar possíveis destinos

# Tecnologias Utilizadas:
• Python<br>
• MySQL<br>
• Flask(previsto para implementação futura)

## Bibliotecas Python(Até o momento)
• mysql.connector(Integrar o Python ao banco MySQL)<br>
• dotenv(Ocultar dados sensíveis)<br>
• os(Para variáveis de ambiente - Complementar dotenv)<br>
• bcrypt(Hasheamento de senhas e validação para login)<br>
• datetime(Conversão para objeto data e verificação de datas válidas.)

# Estrutura do Projeto
Dentro da pasta central app, há a pasta database onde pode se encontrar o script sql para o CRUD de usuários e a criação de tabelas destinations(para destinos) e reservations(para reservas).
A pasta api contém arquivos para ligar o server, definir rotas e configurar JWT.
Interfaces é para fins de teste da ligação com database.
Também há uma pasta de services para aplicar as funções voltadas aos usuários e serviços como um todo.
Além disso possui arquivos utilitários para as necessidades da aplicação.

# Objetivo do Projeto
O objetivo é consolidar na prática conhecimentos de programação e banco de dados por meio do desenvolvimento de um sistema próximo
de uma situação real e desafiadora para meu começo. A aplicação ajuda a entender e executar fundamentos de SQL como CRUD básico, integração MySQL - Python.
Além disso, o projeto serve como base de evolução para atribuição de API utilizando Flask, possibilitando a criação de uma interface Web e 
aprofundando na comunicação entre camadas e manipulação de dados em um contexto mais próximo ao ambiente profissional.
Trata-se de um projeto visando o desenvolvimento pessoal e a possibilidade de dar mais um passo a frente de conseguir
consolidar a minha formação como desenvolvedor.

# Próximos passos
• Finalização da API.<br>
• Posteriormente, desenvolvimento da interface web.