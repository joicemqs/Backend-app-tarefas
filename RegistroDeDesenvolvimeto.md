# Registro de Desenvolvimento

Para desenvolver o backend do projeto estudei de várias formas o Django REST framework e encontrei diversas dificuldades, porém pesquisando, vendo vários tutoriais no youtube e utilizando inteligência artificial consegui executar a tarefa.


A inteligência artificial nesse projeto foi de fundamental importância, pois combinada ao conhecimento adquirido do estudo ela agilizou muito a produção da aplicação. Utilizei os prompts em etapas, por exemplo ao solicitar ajuda com o projeto nunca pedi para que desenvolvesse grandes partes de código ou códigos de diferentes arquivos, perguntando por exemplo "como ficaria um model de usuário no django framework utilizando as melhores práticas", e não utilizando prompts como "Escreva um código em django rest framework para um aplicativo de tarefas". A tomada de decisões foi baseada tanto com base em pesquisas como em inteligência artificial.


Utilizei para me auxiliar a copilot da microsoft, o passo a passo a seguir tem sua participação em todas as partes, não coloquei nesse documento todos os prompts ou respostas por conta da quantidade de passos e etapas do desenvolvimento.
 

## Início do Desenvolvimento


Primeiro comecei criando a pasta backend-tarefas e criei o ambiente virtual com o comando

````
py -m venv api-tarefas
````

Depois ativei o ambiente virtual com

````
api-tarefas\Scripts\activate.bat
````

Com o ambiente ativo, instalei o Django:

````
py -m pip install Django
````

Criei o projeto backend:

````
django-admin startproject backend
````

E criei o app core:

````
python manage.py startapp core
````

Nessa parte acabei ficando confusa em como prosseguir e decidi recomeçar com uma organização diferente

## Refazendo a estrutura

Na pasta todo-backend criei o ambiente virtual:

````
python -m venv .venv
````

Ativei o ambiente virtual:

````
.venv\Scripts\activate.bat
````

Instalei as dependências necessárias:

````
pip install django djangorestframework python-dotenv
````

Criei o projeto core:

````
django-admin startproject core .
````

Criei os apps de contas e de tarefas:

````
python manage.py startapp accounts

python manage.py startapp tasks
````

Criei o arquivo .gitignore com a pasta .venv, porque estava tendo problemas para adicionar os arquivos no git. Em seguida fiz o primeiro commit e conectei com o repositório online do GitHub.

## Desenvolvimento da aplicação

Comecei criando o model de tarefa com todos os campos exigidos, e então o arquivo serializer das tarefas, defini como campos não alteráveis o id da tarefa e o dono.

Desenvolvi a view das tarefas, configurando para que o usuário precise estar autenticado para acessar e adicionei ao INSTALLED_APPS no arquivo settings.py o 'rest framework' e o 'rest_framework.authtoken' para autenticação.Ao tentarfazer as migrações tive problemas com a estrutura de pastas, então reorganizei retirando as pastas tasks e accounts de dentro da pasta core e colocando dentro de uma pasta apps para melhor separação.

Para a autenticação escolhi o simple JWT pela facilidade de implementação e segurança dos tokens, então o instalei no ambiente virtual pelo comando:

````
pip install djangorestframework-simplejwt
````

Decidi recomeçar o desenvolvimento dos models focando primeiro na parte do usuário, já que as tarefas utilizam o id do usuário como chave secundária para garantir o isolamento das informações. Criei o modelo de usuário customizado, desenvolvi os serializers e urls, e atualizei as settings.

Fiz o migrate específico para accounts:

````
python manage.py makemigrations accounts
python manage.py migrate
````

Antes de executar o servidor, criei o superuser:

````
python manage.py createsuperuser
````

Rodei o servidor com o comando e acessei api/accounts/users para visualizar os usuários cadastrados.

````
python manage.py runserver
````

![Lista de usuários](imagens/lista-users-inicial.png)

Testei o endpoint de registro em api/accounts/register para criação de usuários.

![Registro de usuário](imagens/resgistro-usuario.png)

Consultei a lista de usuários novamente e confirmei que o novo usuário aparece registrado.

![Lista com 2 usuários](imagens/lista-usuario-teste.png)

Acessei api/accounts/login e fiz login com o usuário criado, obtendo o token e o refresh token.

![Tokens do login](imagens/token-login.png)

## Desenvolvimento das tarefas

Continuei com o desenvolvimento do app de tarefas começando pelo model, depois implementei os serializers, as views para operações e configurei as URLs das tarefas.

Depois de encontrar alguns erros com a migração resolvi o problema adicionando o arquivo 'tasks' ao INSTALLED_APPS no arquivo setting.py. 

Executei o migrate para atualizar o modelo das tarefas:

````
python manage.py makemigrations tasks

python manage.py migrate
````

Tentei acessar a lista de tarefas, mas precisei de autenticação.

![Tarefas exigindo autenticação](imagens/lista-tarefas-nao-autenticado.png)

Fiz login através de http://127.0.0.1:8000/api/accounts/login/ e obtive o token de autenticação.

Para autenticar pelo navegador, precisei instalar a extensão ModHeader no Chrome, por conta disso o token de login acabou expirando, então aproveitei para utilizar o refresh token para gerar um novo token de acesso.

Com o token renovado consegui acessar as tarefas por meio da extensão e criar uma nova nova tarefa pela própria página.

![Tarefas](imagens/lista%20sem%20tarefa%202.png)

Fiz login com uma conta de teste criada anteriormente para verificar o isolamento dos dados, e ao acessar não foi possível ver a tarefa 1, confirmando que cada usuário só pode visualizar suas próprias tarefas.

![Tarefas isoladas](imagens/tarefas%20email%20teste.png)

Voltei ao cadastro de tarefa com a conta de superusuário e criei uma segunda tarefa para testar a exclusão.

![Deletando tarefa](imagens/deletando%20tarefa.png)

Fui até a lista de tarefas e ela foi deletada com sucesso.

![Tarefa 2 deletada](imagens/lista%20sem%20tarefa%202.png)

Depois disso testei atualizar a tarefa com o PATCH direto na página.

![Atualizando tarefa](imagens/tarefa%201%20modificada.png)

## Recuperação de senha

Com as operações de tarefas funcionando, implementei o sistema de recuperação de senha. Modifiquei o arquivo settings.py para que os emails de recuperação aparecessem no terminal.

Inicialmente o campo de email não aparecia no endpoint de recuperação, então ajustei a view para corrigir esse erro.

Após a correção, consegui digitar o email e receber o token no terminal para redefinir a senha.

![Enviando email par recuperação de senha](imagens/email%20recuperação%20de%20senha.png)

![Reset da senha do usuario teste](imagens/reset%20da%20senha%20do%20usuario%20teste.png)


Testei o login com a nova senha e funcionou perfeitamente, retornando o token de autenticação, o que significa que a senha foi redefinida com sucesso.

## Ajustes Finais

Notei que a função de filtrar datas não estava funcionando corretamente devido ao fuso horário do banco de dados, então ajustei a zona de horário no arquivo settings.py.

Então para melhorar as configurações da aplicação instalei o dotenv no ambiente virtual:

````
npm install dotenv --save
````

Instalei o python-decouple para gerenciar variáveis de ambiente:

````
pip install python-decouple
````

Criei o arquivo .env e atualizei o settings.py para usar as variáveis de ambiente.

Para documentar a API, instalei o drf-spectacular pelo comando abaixo e personalizei a documentação.

````
pip install drf-spectacular
````

Por fim acabei mudando o endpoint das tarefas.




