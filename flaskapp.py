#
# Entry point for the flask server app.
#
from ptapp import create_app
from config import config

#This is so that `flask run` can find the application
flask = create_app(config)

# This is if we run the app itself or through gunicorn?
if __name__ == "__main__":
    flask.run(debug=True)
