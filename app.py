#
# Entry point for the flask server app.
#
import ptapp

#This is so that `flask run` can find the application
flask = ptapp.flaskApp

# This is if we run the app itself or through gunicorn?
if __name__ == "__main__":
 ptapp.flaskApp.run(debug=True)
