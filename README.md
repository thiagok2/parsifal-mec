# Parsifal

Parsifal is a tool to support researchers to perform systematic literature reviews.

A systematic literature review is a secondary study with the objective to identify, analyze and interpret all available evidences from primary studies related to a specific research question. As suggested by Kitchenham and Charters, the activity to perform a systematic literature review involves planning, conducting and reporting the review.

Performing a systematic literature review is a labor-intensive task that requires a huge amount of work from the researcher, designing the protocol, adjusting the search string, filtering the results, sometimes more than a thousand of articles, selecting those articles that attends the include criteria and removing those articles that attends the exclude criteria. After that, the researcher might start to analyze the relevant result one by one.

## License

The source code is released under the [MIT License](https://github.com/vitorfs/parsifal/blob/master/LICENSE).

# Install

## Dev local
#criar ambientes virtuais para instalar python antigo e novo na mesma máquina
https://help.dreamhost.com/hc/en-us/articles/215489338-Installing-and-using-virtualenv-with-Python-2

## criar env
virtualenv --python='/usr/bin/python2.7' parsifal

## Entrar no ambiente
source parsifal/bin/activate

## Sair do ambiente 
deactivate

## passo a passo instalação
https://github.com/vitorfs/parsifal/issues/29

sudo apt-get install python-psycopg2

sudo apt-get install libpq-dev



## configurar arquivo .env

## experiments.txt - alterar
alter psycopg2==2.6 -> 2.7 - requiement.txt

pip install psycopg2-binary

pip install psycopg2 --upgrade

## colocar para rodar
python manage.py runserver

## ignorar owned dos arquivos
git config core.fileMode false

HEAD
# tradução - make/compilação
python manage.py makemessages -l 'sv' -i venv

python manage.py compilemessages



# Configuração com docker

## Prerequisitos:

Instalar docker e docker compose

* https://docs.docker.com/install/

* https://docs.docker.com/compose/install/

Adicionar usuário atual ao grupo docker e relogar

# Construir projeto Docker

docker-compose up --build

Acessar http://localhost:8000

