from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

import src.configuration as config
import src.data_manager as data_manager

# import src.analyze as analyze
import src.stats as stats

app = Flask(__name__)
CORS(app)

headers = {"Content-Type": "application/json"}
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
NOT_FOUND = 404
SERVER_ERROR = 500
NOT_IMPLEMENTED = 501

# MARK: DATA MANAGMENT
@app.route('/api/data/src', methods = ['GET', 'POST', 'DELETE'])
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
        config.set_backup_path(path)
        return make_response('src set', CREATED, headers)

    if request.method == 'DELETE':
        config.del_backup_path()
        return make_response('', NO_CONTENT, headers)

@app.route('/api/data/src/guess', methods = ['GET'])
def guess_source():
    src = data_manager.guess_src()
    content = jsonify(guess = src)
    return make_response(content, OK, headers)

@app.route('/api/data/setup', methods = ['GET', 'POST', 'DELETE'])
def setup():
    if request.method == 'GET':
        prog = data_manager.process_progress()
        if prog == None:
            return make_response('process has not been started', NOT_FOUND, headers)
        response = jsonify(progress = prog)
        return make_response(response, OK, headers)

    if request.method == 'POST':
        success, content = data_manager.process()
        if success == False:
            return make_response(content, SERVER_ERROR, headers)
        result = jsonify(content)
        return make_response(content, CREATED, headers)

    if request.method == 'DELETE':
        config.del_process_progress()
        return make_response('', NO_CONTENT, headers)

# HANDLE ALL STAT REQUESTS
@app.route('/api/stats/contacts', methods = ['GET'])
def contacts():
    n = int(request.args.get('n', 15))
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(start=start, end=end)
    return stats.contacts(msg, n)

@app.route('/api/stats/frequency', methods = ['GET'])
@app.route('/api/stats/<number>/frequency', methods = ['GET'])
def frequency(number=None):
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(start=start, end=end)
    return stats.frequency(msg, number=number, period='M')




# @app.route('/api/convos/summary', methods = ['GET'])
# def api_summary():
#     return stats.summary()
#
# @app.route('/api/convos/frequency', methods = ['GET'])
# @app.route('/api/convos/<number>/frequency', methods = ['GET'])
# def api_frequency(number=None):
#     return stats.frequency(number)

if __name__ == '__main__':
    app.run(debug=True)
