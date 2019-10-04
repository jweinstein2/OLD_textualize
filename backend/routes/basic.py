import src.stats.general as general_stats
from flask import request, jsonify, make_response

import src.data_manager as data_manager

from . import routes

headers = {"Content-Type": "application/json"}
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
NOT_FOUND = 404
SERVER_ERROR = 500
NOT_IMPLEMENTED = 501

@routes.route('/<number>/info', methods = ['GET'])
def contact_info(number):
    content = general_stats.contact(number)
    return make_response(content, OK, headers)

# TODO: this should be quasi-instantaneous
#       move summary data to seperate api call
@routes.route('/numbers', methods = ['GET'])
def contact_summary():
    n = int(request.args.get('n', 100))
    if n == -1: n = None
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(start=start, end=end)
    result = general_stats.contacts_summary(msg, n)
    content = jsonify(result)
    return make_response(content, OK, headers)


