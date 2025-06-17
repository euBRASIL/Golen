# Cluster Node com Django + SVG + HTTP

Este projeto implementa um sistema de gerenciamento de cluster de nós computacionais utilizando Django para o backend e servidor master, uma interface web interativa com mapa do Brasil em SVG, e comunicação HTTP entre o master e os nós workers. Adicionalmente, um programa em C será desenvolvido para gerar automaticamente a estrutura base deste projeto Django.

## 🧩 Funcionalidades Principais

-   **Autenticação de Usuário:** Sistema de login e logout seguro utilizando `django.contrib.auth`.
-   **Interface Web com Mapa Interativo:** Dashboard (`/dashboard/`) que exibe um mapa SVG do Brasil, onde os estados mudam de cor para refletir o status (online/offline) dos nós computacionais localizados neles.
-   **Visualização de Status em Tempo Real:** Atualização automática do mapa e da lista de nós no dashboard via polling AJAX, fornecendo uma visualização próxima do tempo real.
-   **API RESTful para Comunicação:** Endpoints para registro de nós, atribuição de tarefas e atualização de status.
-   **Simulação de Nós Workers:** Script `worker.py` que simula múltiplos nós computacionais se conectando ao master.
-   **Banco de Dados:** Configurado para SQLite por padrão, com flexibilidade para usar PostgreSQL.
-   **Administração via Django Admin:** Interface para gerenciar os nós registrados.
-   **(Futuro) Gerador de Projeto em C:** Um programa em C (`cluster_django.c`) para criar automaticamente o esqueleto do projeto Django.

## 🛠️ Arquitetura e Descrição Técnica

O sistema é composto por um servidor master (aplicação Django) e múltiplos nós workers (simulados por `worker.py`).

### 1. Servidor Master (Aplicação Django)

-   **Projeto Django:** `cluster_node`
-   **App Principal:** `nodes` (gerencia informações e interações dos nós)

#### Estrutura do Projeto Django:
```
cluster_node/
├── manage.py
├── requirements.txt
├── worker.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   └── mapa_brasil.svg
├── static/
│   └── css/
│       └── style.css
├── nodes/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── migrations/
└── cluster_node/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

#### Componentes Chave do Django:

-   **`nodes/models.py`**:
    -   Define o modelo `Node` com os seguintes campos:
        -   `id`: UUIDField (chave primária, gerado automaticamente).
        -   `ip`: GenericIPAddressField (endereço IP do nó).
        -   `location`: CharField (localização do nó, ex: 'SP', 'RJ', usado para o mapa).
        -   `status`: CharField (choices: 'online', 'offline', default: 'offline').
        -   `last_update`: DateTimeField (atualizado automaticamente quando o nó envia um status).

-   **`nodes/views.py`**:
    -   `dashboard_view`: Requer login, busca todos os nós e os envia para `dashboard.html`.
    -   **API Views (usando Django REST Framework):**
        -   `NodeListAPIView` (`GET /api/nodes/`): Lista todos os nós. Requer autenticação (usado pelo dashboard).
        -   `NodeRegisterAPIView` (`POST /api/register/`): Permite que novos nós se registrem. Aberto.
        -   `NodeTaskAPIView` (`GET /api/task/`): Endpoint para nós solicitarem tarefas. Aberto. Retorna uma tarefa de exemplo.
        -   `NodeStatusUpdateAPIView` (`POST /api/status/`): Permite que nós atualizem seu status. Aberto.

-   **`nodes/serializers.py`**:
    -   `NodeSerializer`: Para serialização geral de instâncias `Node`.
    -   `NodeRegistrationSerializer`: Usado por `NodeRegisterAPIView` para lidar com os campos `ip` e `location` no registro.

-   **`nodes/urls.py`**: Define as rotas para o `dashboard_view` e para os endpoints da API.
-   **`cluster_node/urls.py`**: Define as rotas globais, incluindo autenticação (`login/`, `logout/`), página inicial (`index.html`), e inclui as URLs do app `nodes`.
-   **`cluster_node/settings.py`**:
    -   `INSTALLED_APPS`: Inclui `'nodes.apps.NodesConfig'`, `'rest_framework'`.
    -   `TEMPLATES['DIRS']`: Configurado para `[BASE_DIR / 'templates']`.
    -   `STATICFILES_DIRS`: Configurado para `[BASE_DIR / 'static']`.
    *   `LOGIN_URL = '/login/'`: Redireciona para a página de login customizada.
    *   `LOGIN_REDIRECT_URL = '/dashboard/'`: Redireciona para o dashboard após login bem-sucedido.
    -   `DATABASES`: Configurado para SQLite por padrão.

-   **`templates/`**:
    -   `base.html`: Template base com navegação (Home, Login/Logout, Dashboard).
    -   `index.html`: Página inicial pública.
    -   `login.html`: Formulário de login.
    -   `dashboard.html`: Exibe a lista de nós e o mapa SVG interativo. Inclui JavaScript para polling AJAX.
    -   `mapa_brasil.svg`: Arquivo SVG do mapa do Brasil com IDs de estados para interatividade.

### 2. API RESTful

A comunicação entre os nós workers e o servidor master é feita via uma API REST.

-   **`GET /api/nodes/`**
    -   **Descrição:** Lista todos os nós registrados.
    -   **Autenticação:** Requerida (sessão).
    -   **Resposta Exemplo (200 OK):**
        ```json
        [
            {
                "id": "some-uuid-string",
                "ip": "192.168.1.10",
                "location": "SP",
                "status": "online",
                "last_update": "2023-10-27T10:20:30.400Z"
            }
        ]
        ```

-   **`POST /api/register/`**
    -   **Descrição:** Permite que um novo nó se registre no master.
    -   **Autenticação:** Nenhuma.
    -   **Payload Exemplo:**
        ```json
        {
            "ip": "192.168.1.15",
            "location": "RJ"
        }
        ```
    -   **Resposta Exemplo (201 Created):**
        ```json
        {
            "id": "new-uuid-string",
            "ip": "192.168.1.15",
            "location": "RJ",
            "status": "online", /* Definido automaticamente no registro */
            "last_update": "2023-10-27T10:22:30.500Z"
        }
        ```

-   **`GET /api/task/`**
    -   **Descrição:** Um nó solicita uma nova tarefa ao master.
    -   **Autenticação:** Nenhuma.
    -   **Resposta Exemplo (200 OK):** (Atualmente retorna uma tarefa de exemplo)
        ```json
        {
            "task_id": "task_123",
            "type": "simple_math",
            "instruction": "Add the numbers.",
            "data": { "a": 10, "b": 25 }
        }
        ```

-   **`POST /api/status/`**
    -   **Descrição:** Um nó envia uma atualização de seu status para o master.
    -   **Autenticação:** Nenhuma.
    -   **Payload Exemplo:**
        ```json
        {
            "ip": "192.168.1.15", /* Usado para identificar o nó */
            "status": "online" /* ou "offline" */
            /* ,"task_result": { ... } // Para futuras implementações */
        }
        ```
    -   **Resposta Exemplo (200 OK):** (Retorna os dados atualizados do nó)
        ```json
        {
            "id": "node-uuid-string",
            "ip": "192.168.1.15",
            "location": "RJ",
            "status": "online",
            "last_update": "2023-10-27T10:25:30.600Z"
        }
        ```

### 3. Node Worker (`worker.py`)

-   **Propósito:** Um script Python que simula um nó computacional.
-   **Funcionamento:**
    1.  **Configuração:** Define o endereço do servidor master, seu próprio IP (simulado/aleatório) e localização (aleatória de uma lista de estados brasileiros).
    2.  **Registro:** Ao iniciar, tenta se registrar no master enviando um POST para `/api/register/`.
    3.  **Polling de Status:** Periodicamente (a cada 30s), envia seu status ('online') para `/api/status/`.
    4.  **Polling de Tarefas:** Periodicamente (a cada 60s), solicita uma nova tarefa do master via GET em `/api/task/`.
    5.  **Processamento de Tarefa:** Se uma tarefa é recebida (ex: cálculo matemático simples), ele a processa e exibe o resultado no console.
    6.  **Desligamento:** Tenta enviar um status 'offline' ao ser encerrado.
-   **Execução:** Pode ser executado múltiplas vezes para simular vários nós: `python worker.py`.

### 4. Frontend (Dashboard Interativo)

-   **Localização:** `templates/dashboard.html`
-   **Funcionalidades:**
    -   Exibe uma tabela com os nós registrados (ID, IP, Localização, Status, Última Atualização).
    -   Incorpora o `mapa_brasil.svg`.
    -   Utiliza JavaScript para:
        -   Buscar dados dos nós da API (`/api/nodes/`) a cada 10 segundos (polling AJAX).
        -   Atualizar a cor de preenchimento dos estados no SVG (`.online` para verde, `.offline` para vermelho) com base no status do nó correspondente à localização (ID do estado no SVG).
        -   Atualizar dinamicamente a tabela de nós.

## 📦 Como Instalar e Executar

### Pré-requisitos
-   Python 3.8+
-   pip (Python package installer)

### Passos para Instalação
1.  **Clone o repositório (exemplo):**
    \`\`\`bash
    git clone https://github.com/seu_usuario/cluster_node.git # Substitua pelo URL real do repositório
    cd cluster_node
    \`\`\`

2.  **Crie e ative um ambiente virtual:**
    \`\`\`bash
    \python -m venv venv
    # Linux/Mac
    \source venv/bin/activate
    # Windows
    # venv\Scripts\activate
    \`\`\`

3.  **Instale as dependências:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
    Isso instalará Django, Django REST Framework, Requests, etc.

4.  **Aplique as migrações do banco de dados:**
    \`\`\`bash
    python manage.py migrate
    \`\`\`

5.  **Crie um superusuário (para acesso ao admin e login inicial):**
    \`\`\`bash
    python manage.py createsuperuser
    \`\`\`
    Siga as instruções para definir nome de usuário, email e senha.

6.  **Rode o servidor de desenvolvimento Django (Master):**
    \`\`\`bash
    python manage.py runserver
    \`\`\`
    O servidor master estará acessível em \`http://localhost:8000/\`.

### Executando os Nós Workers
Em um ou mais terminais separados (com o ambiente virtual ativado), execute o script \`worker.py\`:
\`\`\`bash
python worker.py
\`\`\`
Cada instância do \`worker.py\` simulará um nó diferente, registrando-se no master e enviando atualizações.

## 🖥️ Acessando a Interface Web

-   **Página Inicial:** \`http://localhost:8000/\`
-   **Login:** \`http://localhost:8000/login/\`
    -   Use as credenciais do superusuário criado anteriormente.
-   **Dashboard:** \`http://localhost:8000/dashboard/\`
    -   Após o login, você será redirecionado para o dashboard.
    -   Observe os nós registrados pelos workers aparecerem na lista.
    -   O mapa do Brasil deverá colorir os estados correspondentes às localizações dos nós online/offline.
-   **Admin Django:** \`http://localhost:8000/admin/\`
    -   Interface administrativa para gerenciar os nós e outros dados do Django.

## 📄 (Opcional) Código C – Gerador de Estrutura (Futuro)

Este projeto também incluirá um programa em C (\`cluster_django.c\`) projetado para gerar automaticamente a estrutura de diretórios e arquivos base do projeto Django.
\`\`\`bash
# Compilar (exemplo Linux/macOS com GCC)
gcc cluster_django.c -o cluster_django_generator
# Executar
./cluster_django_generator
\`\`\`
Este gerador visa facilitar o setup inicial e garantir a consistência da estrutura do projeto. (Mais detalhes quando a Parte 2 do projeto for implementada).

## 📝 Créditos

Desenvolvido com base na integração entre Django, Python, JavaScript, SVG, e conceitos de sistemas distribuídos. Inspirado pela necessidade de visualização e controle de clusters computacionais.
