# our base image
FROM python:2.7

RUN apt-get update && apt-get install -y postgresql-client gettext

RUN pip install psycopg2 --user
RUN pip install psycopg2-binary --user

COPY requirements.txt /app/
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt --user


COPY . /app
# Define environment variable
ENV NAME World

