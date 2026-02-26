# Prints de Testes da API no Postman(Cadastro de Usuário, Login e Criação de uma Reserva)

- Erro de formatação de email
![email_format_error](imgs/postman_tests/email_format_error.png)
- Email que já está sendo utilizado
![email_already_used](imgs/postman_tests/email_already_used.png)
- Erro de confirmação da senha
![password_confirm_error](imgs/postman_tests/password_confirm_error.png)
- Data para criação de conta inválida
![invalid_birth_date](imgs/postman_tests/invalid_birth_date.png)
- Com todos dados sem erro de formato/confirmação é possível fazer o login
![successful_login](imgs/postman_tests/successful_login.png)
- Tentativa de criar reserva sem token
![missing_token_error](imgs/postman_tests/missing_token_error.png)
- Criação da reserva com token
![reservation_created](imgs/postman_tests/reservation_created.png)