# Documentação do Projeto MVP Bucho Cheio
Este documento fornece uma visão geral completa do sistema MVP, incluindo sua arquitetura, como configurá-lo, a estrutura do banco de dados, as rotas da API e a funcionalidade de cada módulo.
### 🚀 Visão Geral do Projeto
Este projeto é um sistema de gerenciamento de reservas de almoço, focado em um MVP (Produto Mínimo Viável). Ele permite que usuários se cadastrem, façam login, reservem vagas de almoço para o dia seguinte e realizem check-in via QR Code. Administradores têm funcionalidades adicionais para criar vagas e gerenciar candidaturas a vagas de refeições.
### 🛠️ Configuração e Instalação
Para configurar e rodar o projeto localmente, siga os passos abaixo:
##### Pré-requisitos
Certifique-se de ter o Python 3.x e o pip (gerenciador de pacotes do Python) instalados em sua máquina.
1. Clonar o Repositório
git clone https://github.com/EmerSormany/bucho-cheio.git
2. cd bucho-cheio
3. Criar e Ativar o Ambiente Virtual
É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```
python3 -m venv venv
```
```
source venv/bin/activate  -- No Linux/macOS
```
```
venv\Scripts\activate   -- No Windows (cmd.exe)
```
```
.\venv\Scripts\Activate.ps1 -- No Windows (PowerShell)
```

4. Instalar as Dependências
Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no requirements.txt:
```
pip install -r requirements.txt
```

6. Rodar a Aplicação
Com o ambiente virtual ativado, você pode iniciar o servidor Flask:
```
flask run
```

A aplicação estará disponível em http://127.0.0.1:5000/ (ou outra porta indicada pelo Flask).

### 🗄️ Estrutura do Banco de Dados
##### O sistema utiliza um banco de dados SQLite com as seguintes tabelas:

###### 🧑‍💻 Tabela: `usuarios`

Armazena informações sobre os usuários do sistema.

| Coluna         | Tipo     | Restrições                     | Descrição                                                   |
|----------------|----------|--------------------------------|-------------------------------------------------------------|
| `id`           | INTEGER  | PRIMARY KEY AUTOINCREMENT      | ID único do usuário.                                        |
| `nome`         | TEXT     | NOT NULL                       | Nome completo do usuário.                                   |
| `email`        | TEXT     | UNIQUE NOT NULL                | Endereço de e-mail do usuário (único).                      |
| `senha_hash`   | TEXT     | NOT NULL                       | Hash da senha do usuário (para segurança).                  |
| `administrador`| INTEGER  | NOT NULL (0 = Falso, 1 = Verdadeiro) | Indica se o usuário tem privilégios de administrador. |
| `matricula`    | TEXT     | UNIQUE NOT NULL                | Número de matrícula do usuário (único).                     |
| `curso`        | TEXT     | —                              | Curso do usuário.                                           |

###### 📅 Tabela: `quadro_vagas`

Armazena a quantidade de vagas de almoço disponíveis para datas específicas.

| Coluna        | Tipo    | Restrições                            | Descrição                                                  |
|---------------|---------|----------------------------------------|------------------------------------------------------------|
| `id`          | INTEGER | PRIMARY KEY AUTOINCREMENT              | ID único do registro de vagas.                             |
| `data_vagas`  | TEXT    | NOT NULL UNIQUE (formato 'YYYY-MM-DD') | Data para a qual as vagas estão disponíveis.               |
| `quantidade`  | INTEGER | NOT NULL                               | Número de vagas disponíveis para a data.                   |

###### 📌 Tabela: `reserva`

Registra as reservas de almoço feitas pelos usuários.

| Coluna        | Tipo    | Restrições                                                                 | Descrição                                                    |
|---------------|---------|----------------------------------------------------------------------------|--------------------------------------------------------------|
| `usuario_id`  | INTEGER | FOREIGN KEY REFERENCES `usuarios(id)`                                      | ID do usuário que fez a reserva.                             |
| `vaga_id`     | INTEGER | FOREIGN KEY REFERENCES `quadro_vagas(id)`                                  | ID da vaga associada a esta reserva.                         |
| `situacao`    | TEXT    | NOT NULL CHECK (`situacao` IN ('ativa', 'cancelada', 'usada', 'pendente')) | Status atual da reserva.                                     |
| `qr_code`     | TEXT    | NOT NULL UNIQUE                                                            | String Base64 do QR Code gerado para a reserva.              |
| `chekin`      | TEXT    | DEFAULT NULL (formato 'YYYY-MM-DD HH:MM:SS')                               | Timestamp do check-in, se realizado.                         |
| `pk_reserva`  | —       | PRIMARY KEY (`usuario_id`, `vaga_id`)                                      | Chave primária composta.                                     |


### 🌐 Rotas da Aplicação (API)
As rotas são definidas usando Flask Blueprints e MethodView para organizar o código.
#### Rotas Públicas
#### GET / - Página Inicial
* **Descrição:** Exibe a página de boas-vindas do sistema.
* **View:** IndexView
#### GET /user - Formulário de Cadastro de Usuário
* **Descrição:** Renderiza o formulário para novos usuários se cadastrarem.
* **View:** UserView
#### POST /user - Cadastro de Novo Usuário
* **Descrição:** Recebe os dados do formulário de cadastro, valida o e-mail (verifica se já existe) e cria um novo registro de usuário no banco de dados.
* **View:** UserView
* **Parâmetros do Formulário:** name, email, password, matriculation, course, admin (checkbox, 0 ou 1).
#### GET /login - Formulário de Login
* **Descrição:** Renderiza o formulário para os usuários fazerem login.
* **View:** LoginView
#### POST /login - Autenticação do Usuário
* **Descrição:** Recebe as credenciais do formulário, autentica o usuário. Se o login for bem-sucedido, armazena o user_id e admin (se aplicável) na sessão e redireciona para a página apropriada (/panel para admin, /home para usuário comum).
* **View:** LoginView
* **Parâmetros do Formulário:** email, password.
#### POST /logout - Logout
* **Descrição:** Remove o user_id e admin da sessão, efetivando o logout do usuário e redirecionando para a página inicial.
* **View:** LogoutView
#### Rotas Protegidas (Requerem Autenticação)
#### GET /home - Página Principal do Usuário
* **Descrição:** Página acessível apenas por usuários logados.
* **View:** HomeView
* **Proteção:** @Auth.login_required
#### GET /reservation - Formulário de Reserva
* **Descrição:** Exibe o formulário para o usuário fazer uma reserva. Os campos são pré-preenchidos com os dados do usuário logado.
* **View:** ReservationView
* **Proteção:** @Auth.login_required
#### POST /reservation - Criação de Reserva
* **Descrição:** Processa a solicitação de reserva. Verifica a disponibilidade de vagas para o dia seguinte (regra de negócio: reserva para o dia +1), gera um QR Code único para a reserva e a salva no banco de dados com status 'pendente'.
* **View:** ReservationView
* **Proteção:** @Auth.login_required
#### GET /checkin - Geração de QR Code para Check-in
* **Descrição:** Busca a reserva ativa do usuário logado para a data atual. Se uma reserva for encontrada com status 'ativa', um QR Code contendo usuario_id e vaga_id é gerado e exibido na tela para o check-in. Caso contrário, uma mensagem de "não há reserva" é exibida.
* **View:** ChekinView
* **Proteção:** @Auth.login_required
#### Rotas de Administração (Requerem Autenticação e Permissão de Admin)
#### GET /vacancies - Formulário de Cadastro de Vagas
* **Descrição:** Exibe o formulário para administradores cadastrarem novas vagas de almoço.
* **View:** VacanciesView
* **Proteção:** @Auth.login_required, @Auth.admin_required
#### POST /vacancies - Criação de Vagas
* **Descrição:** Recebe a data e quantidade de vagas do formulário e as registra na tabela quadro_vagas.
* **View:** VacanciesView
* **Proteção:** @Auth.login_required, @Auth.admin_required
* **Parâmetros do Formulário:** date, quantity.
#### GET /admin - Painel de Administração
* **Descrição:** Permite que administradores busquem e visualizem todas as candidaturas a vagas de almoço por uma data específica. Se nenhuma data for fornecida, exibe o painel vazio.
* **View:** AdminView
* **Proteção:** @Auth.login_required, @Auth.admin_required
* **Parâmetros de Consulta:** date.
#### POST /admin - Atualização de Reservas no Painel
* **Descrição:** Processa as alterações de status das reservas feitas no painel de administração. A lógica verifica o status atual da reserva antes de aplicar a mudança:
  * Se a nova situação for 'ativa' e a anterior era 'pendente' ou 'cancelada': Aprova a reserva e decrementa a quantidade de vagas.
  * Se a nova situação for 'cancelada' e a anterior era 'ativa': Cancela a reserva e incrementa a quantidade de vagas (libera a vaga).
  * Se a nova situação for 'cancelada' e a anterior era 'pendente': Cancela a reserva sem alterar a quantidade de vagas.
* **View:** AdminView
* **Proteção:** @Auth.login_required, @Auth.admin_required
* **Parâmetros do Formulário:** total_lines (número total de linhas na tabela), user_id_{i}, vacancy_id_{i}, new_situation_{i} (para cada linha i).
  
### 🧩 Módulos e Funcionalidades

**db/database.py**

* **Função:** Gerencia a conexão com o banco de dados SQLite.
* **Principais Funções:**
  * **get_db_connection():** Abre e retorna uma conexão com o banco de dados.
  * **close_db():** Fecha a conexão com o banco de dados.
  * **init_db_schema():** Inicializa o esquema do banco de dados a partir do arquivo schema.sql.
    
**models/Admin.py**

* **Função:** Contém a lógica de negócios para as operações administrativas relacionadas às reservas.
* **Principais Métodos:**
  * **list_applications_by_date(data):** Lista todas as candidaturas (reservas) para uma data específica, juntando dados de usuários e vagas.
  * **approve_application(usuario_id, vaga_id):** Altera o status de uma reserva para 'ativa' e decrementa a quantidade de vagas disponíveis.
  * **deny_application(usuario_id, vaga_id):** Altera o status de uma reserva para 'cancelada' (usado para reservas pendentes).
  * **deny_application_aproved(usuario_id, vaga_id):** Altera o status de uma reserva para 'cancelada' e incrementa a quantidade de vagas (usado para reservas ativas).

**models/Login.py**

* **Função:** Lida com a lógica de autenticação de usuários.
* **Principais Métodos:**
  * **login(user, password):** Verifica a senha fornecida com o hash armazenado e retorna os dados do usuário se a autenticação for bem-sucedida.
  * **get_user_by_email(email):** Busca um usuário no banco de dados pelo e-mail.

**models/Reservation.py**

* **Função:** Gerencia as operações relacionadas às reservas de almoço.
* **Principais Métodos:**
  * **__init__(self, user_id, vacancy_id, qr_code):** Construtor para criar um objeto de reserva.
  * **save():** Salva uma nova reserva no banco de dados com status 'pendente'.
  * **get_aplication_status(user_id, vacancy_id):** Retorna o status atual de uma reserva específica.
  * **get_reservation(user_id):** Busca a reserva de um usuário, juntando dados da vaga para obter a data.

**models/User.py**

* **Função:** Gerencia as operações relacionadas aos usuários.
* **Principais Métodos:**
  * **__init__(self, name, email, password, admin, matriculation, course):** Construtor para criar um objeto de usuário.
  * **hash_password(password):** Gera um hash seguro para a senha.
  * **create_user():** Salva um novo usuário no banco de dados.
  * **get_user_by_id(user_id):** Busca um usuário no banco de dados pelo ID.

**models/Vacancies.py**

* **Função:** Gerencia as operações relacionadas às vagas de almoço.
* **Principais Métodos:**
  * **__init__(self, date, vacancies):** Construtor para criar um objeto de vaga.
  * **create_vacancy():** Salva novas vagas no quadro_vagas.
  * **get_vacancies_by_date(date):** Retorna o ID de um registro de vaga para uma data específica.

**utils/Auth.py**

* **Função:** Fornece decoradores para proteção de rotas, garantindo que apenas usuários autenticados ou administradores possam acessá-las.
* **Principais Métodos:**
  * **login_required(f):** Decorador que exige que o usuário esteja logado para acessar a rota.
  * **admin_required(f):** Decorador que exige que o usuário seja um administrador para acessar a rota.
  * **load_logged_user():** Carrega os dados do usuário logado no objeto g do Flask.

**utils/QRcode.py**

* **Função:** Lida com a geração e leitura de QR Codes.
* **Principais Métodos:**
  * **generate_qr_code(usuario_id, vaga_id):** Gera um QR Code contendo o ID do usuário e o ID da vaga, retornando-o como uma string Base64.
  * **read_qr_code(qr_code_base64):** (Este método precisaria ser implementado conforme a nossa discussão anterior) Lê um QR Code a partir de uma string Base64 da imagem e retorna os dados decodificados.
### 📦 Dependências do Projeto (requirements.txt)
As seguintes bibliotecas Python são utilizadas no projeto:
* Flask==3.1.0: O microframework web principal.
* qrcode[pil]==8.2: Para geração de QR Codes, incluindo a dependência Pillow para manipulação de imagens.
* Pillow==11.1.0: Biblioteca de processamento de imagens (já incluída com qrcode[pil]).
* Werkzeug==3.1.3: Um kit de ferramentas WSGI para Python (usado pelo Flask, incluindo funcionalidades de segurança como hashing de senhas).
* pyzbar==0.1.9: Para leitura e decodificação de QR Codes a partir de imagens.
