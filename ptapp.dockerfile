from python:3.7.4-slim-buster
LABEL maintainer="Scott McKittrick"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
   && pip install -r requirements.txt

#Copying the files instead of the module
#fix this later.
COPY ptapp/* ./

EXPOSE 8000

# using the flask server for now. Switch to guicorn later.
# https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose
CMD [ "flask", "run", "--host=0.0.0.0", "--port=8000"]
