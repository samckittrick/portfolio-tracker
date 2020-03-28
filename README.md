# portfolio-tracker
Application to track my stock portfolio

Running with Docker Compose  
`sudo docker-compose --file portfolio-tracker-compose.yml up`

Running the celery worker outside of Docker (requires docker compose ports to be exported)  
`celery worker -A ptapp.app.celery --loglevel=info`

Running the flask app from outside Docker  
`FLASK_APP=ptapp/app.py flask run --host=0.0.0.0 --port=8000`
