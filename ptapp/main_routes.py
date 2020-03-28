#
# Place to define flask routes.
#
from flask import Blueprint, current_app
from .tasks import long_task
import json

# Using flask blueprints to allow for splitting up of modules
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    print(current_app.config)
    return "This is the env you're looking for:"
@main_routes.route('/start')
def starttask():
    task = long_task.apply_async()
    return "This is the task you are looking for %s" % task.id
