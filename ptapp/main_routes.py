#
# Place to define flask routes.
#
from flask import Blueprint
from .tasks import long_task

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return "This is the droid you're looking for"

@main_routes.route('/start')
def starttask():
    task = long_task.apply_async()
    return "This is the task you are looking for %s" % task.id
