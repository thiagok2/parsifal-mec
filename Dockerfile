# our base image
FROM python:2.7

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY . /app

RUN pip install psycopg2 --user
RUN pip install psycopg2-binary --user
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt --user

# Make port 8080 available to the world outside this container
#EXPOSE 8080

# Define environment variable
ENV NAME World

