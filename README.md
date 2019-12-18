# Parsifal

Parsifal is a tool to support researchers to perform systematic literature reviews.

A systematic literature review is a secondary study with the objective to identify, analyze and interpret all available evidences from primary studies related to a specific research question. As suggested by Kitchenham and Charters, the activity to perform a systematic literature review involves planning, conducting and reporting the review.

Performing a systematic literature review is a labor-intensive task that requires a huge amount of work from the researcher, designing the protocol, adjusting the search string, filtering the results, sometimes more than a thousand of articles, selecting those articles that attends the include criteria and removing those articles that attends the exclude criteria. After that, the researcher might start to analyze the relevant result one by one.

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

