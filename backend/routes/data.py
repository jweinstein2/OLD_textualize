from flask import request, jsonify, make_response
import os

import src.configuration as config
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

# MARK: DATA MANAGMENT
@routes.route('/data/state', methods = ['GET'])
def get_state():
    status, additional = data_manager.process_progress()
    if status == "completed":
        state = 3
    elif status == "failed":
        state = 2
    elif status == "in_progress":
        state = 2
    elif status == "unstarted":
        state = 1
    else:
        print("unexpected state")
        state = 0

    return make_response(jsonify({'state': state}), OK, headers)


@routes.route('/data/src', methods = ['GET', 'POST', 'DELETE'])
def src():
    if request.method == 'GET':
        path = config.get_backup_path()
        success = path != None and path != ''

        if success:
            response = jsonify(path = path)
            return make_response(response, OK, headers)

        guess = data_manager.guess_src()
        response = jsonify(description = "missing: data path currently unset",
                           possibilities = guess)
        return make_response(response, NOT_FOUND, headers)

    if request.method == 'POST':
        path = request.form['value']

        if not os.path.isdir(path):
            return make_response('invalid directory path', BAD_REQUEST, headers)

        config.set_backup_path(path)
        return make_response('src set', CREATED, headers)

    if request.method == 'DELETE':
        config.del_backup_path()
        config.del_process_progress()
        data_manager.clear()
        return make_response('', NO_CONTENT, headers)

@routes.route('/api/data/src/guess', methods = ['GET'])
def guess_source():
    src = data_manager.guess_src()
    content = jsonify(guess = src)
    return make_response(content, OK, headers)

@routes.route('/api/data/setup', methods = ['GET', 'POST', 'DELETE'])
def setup():
    if request.method == 'GET':
        status, msg = data_manager.process_progress()
        response = jsonify({"status": status, "message": msg})
        return make_response(response, OK, headers)

    if request.method == 'POST':
        path = config.get_backup_path()
        success, content = data_manager.process(path)
        if not success:
            return make_response(content, SERVER_ERROR, headers)
        result = jsonify(content)
        return make_response(result, CREATED, headers)

    if request.method == 'DELETE':
        config.del_last_error()
        config.del_process_progress()
        return make_response('', NO_CONTENT, headers)

