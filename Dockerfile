# our base image
FROM python:2.7

RUN apt-get update && apt-get install -y postgresql-client gettext libatk1.0-0 libgtk2.0-0 libpango1.0-0 python-gtk2 

ADD http://ftp.br.debian.org/debian/pool/main/g/gnome-python-desktop/python-rsvg_2.32.0+dfsg-3_amd64.deb /app/python-rsvg_2.32.0+dfsg-3_amd64.deb
RUN dpkg -i /app/python-rsvg_2.32.0+dfsg-3_amd64.deb
RUN pip install psycopg2 --user
RUN pip install psycopg2-binary --user

COPY requirements.txt /app/
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt --user


COPY . /app
# Define environment variable
ENV NAME World

