# Backend Todo-app

Essa é uma aplicação construída para ser utilizada no backend do aplicativo de tarefas, nela foi utilizada o Django Rest Framework para desenvolvimento e drf spectacular para documentação.

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

## Pré-requisitos
Antes de instalar e executar a aplicação, certifique-se de ter os seguintes requisitos atendidos:

### Ambiente de desenvolvimento

Python 3.10 ou superior Linguagem principal utilizada no projeto. O instalador do Python pode ser baixado pelo site oficial tanto para Windows quanto para MacOS ou Linux em:

https://www.python.org/downloads/

Para usuários de Windows o Python pode ser instalado diretamente da Microsoft Store, forma recomendada para a maioria dos usuários segundo a própria página de download do site.

Após instalação para consultar a versão instalada Podemos utilizar no cmd o comando:

````
python –version
````

E em seguida a versão será exibida.

### pip

pip Gerenciador de pacotes do Python. Já vem instalado com o Python em versões recentes.

Virtualenv (opcional, mas recomendado) Para criar ambientes isolados. Instale com:

````
pip install virtualenv
````
### Git
Para controle do versionamento foi utilizada a ferrmaenta Git que pode ser baixada em diferentes sistemas operacionais pelo link a seguir:

https://git-scm.com/downloads

### Visual Studio Code

Para executar os programas foi utilizado o software Visual Studio Code disponível para download em:

https://code.visualstudio.com/download

Extensões recomendadas para VSCode:

Python (Microsoft)

Django

REST Client ou Thunder Client (para testar endpoints)

### Dendências do projeto:

Django – framework web principal

djangorestframework – para criação de APIs REST

djangorestframework-simplejwt – autenticação via JWT

drf-spectacular – documentação automática da API

SQLite (padrão do Django, já incluído)

Instalação listada na sessão seguinte


## Instalação e execução da API

Siga os passos abaixo para configurar e executar o projeto localmente:

### 1. Clonar o repositório
```
git clone https://github.com/joicemqs/Backend-app-tarefas

cd seu-projeto
```
### 2. Criar e ativar ambiente virtual
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular
```

### 4. Configurar variáveis de ambiente
Crie um arquivo .env com suas configurações locais, com base no arquivo env.example.txt, como:

```
SECRET_KEY=seu-segredo
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
Adicione ao ALLOWED_HOSTS o IP do computador utilizado para rodar o servidor do Django

### 5. Aplicar migrações
````
python manage.py makemigrations accounts
python manage.py migrate

python manage.py makemigrations tasks
python manage.py migrate
````

### 6. Criar superusuário
````
python manage.py createsuperuser
````
Em seguida siga inserindo os dados do super usuário

### 7. Rodar o servidor de desenvolvimento
````
python manage.py runserver
````

A API estará disponível em http://127.0.0.1:8000/.


### 8. Acessar a documentação da API
Se estiver usando drf-spectacular, acesse:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/redoc/

Schema JSON: http://127.0.0.1:8000/api/schema/

### 9. Executar suíte de testes

Para executar os testes automáticos execute os comandos abaixo no raiz do projeto

````
python manage.py test apps/accounts/tests

python manage.py test apps/tasks/tests

````

## Licença

[MIT](https://choosealicense.com/licenses/mit/)