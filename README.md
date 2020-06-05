# Sumarize

A plataforma Sumarize trata-se de uma plataforma Web voltada para construção de revisões sistemáticas e meta-análises. Trata-se de uma aplicação web construída em python, sustentada com o framework WEB/MVC Django, com um front-end fortemente baseado em javascript com a biblioteca jQuery. A plataforma tem como característica a responsividade apoiada no framework Bootstrap. A comunicação entre os componentes cliente/servidor da aplicação é baseada em templates do Django e REST com ajax do jQuery. 
A fim de possibilitar o acesso da plataforma com as fontes de dados ScienceDirect e Scopus, a plataforma Sumarize realiza acesso às respectivas bases a partir de uma biblioteca REST disponibilizada pelo próprio Django. Por fim, de modo a possibilitar a renderização dos elementos gráficos, necessários à execução da meta-análise faz-se uso da linguagem de programação R, acessada diretamente pelo Django a partir de chamadas REST.


## License

The source code is released under the [MIT License](https://github.com/vitorfs/parsifal/blob/master/LICENSE).

# Install
## criar env

Instalar python 2.7
Instalar virtualenv

sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev

git clone
git config core.fileMode false

#criar database parsifal
criar database parsifal e usuario parsifal

Copiar/Criar .env

#criar virtualenv
virtualenv --python='/usr/bin/python2.7' parsifal

# acessar virtualenv
source parsifal/bin/activate

pip install -r requirements.txt

python manage.py runserver

# Virtualenv
## Entrar no ambiente
source parsifal/bin/activate

## Sair do ambiente 
deactivate



# Tradução - make/compilação
python manage.py makemessages -l 'sv' -i venv

python manage.py compilemessages


# Alteração no modelo/banco de dados

python manage.py makemigrations

python manage.py migrate


# Configuração com docker

## Prerequisitos:

Instalar docker e docker compose

* https://docs.docker.com/install/

* https://docs.docker.com/compose/install/

Adicionar usuário atual ao grupo docker e relogar

# Construir projeto Docker

docker-compose up --build

Acessar http://localhost:8000


# Rodar

source parsifal/bin/activate

python manage.py runserver
