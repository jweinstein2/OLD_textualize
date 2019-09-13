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
        return make_response(result, CREATED, headers)

    if request.method == 'DELETE':
        config.del_process_progress()
        return make_response('', NO_CONTENT, headers)

# HANDLE ALL STAT REQUESTS

# return n most frequent handles by total sent / received
# TODO: add sort by sent and received
@app.route('/api/handles', methods = ['GET'])
def handles():
    n = int(request.args.get('n', 15))
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(start=start, end=end)
    result = stats.handles(msg, n)
    content = jsonify(result)
    return make_response(content, OK, headers)

@app.route('/api/stats/frequency', methods = ['GET'])
@app.route('/api/stats/<handle>/frequency', methods = ['GET'])
def frequency(handle=None):
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    period = request.args.get('period', 'M')
    if handle is not None:
        try:
            handle = int(handle)
        except ValueError:
            return make_response('invalid handle', NOT_FOUND, headers)

    msg = data_manager.messages(handle=handle, start=start, end=end)
    result = stats.frequency(msg, period=period)
    return make_response(result, OK, headers)


@app.route('/api/stats/emoji', methods = ['GET'])
@app.route('/api/stats/<handle>/emoji', methods = ['GET'])
def emoji(handle=None):
    n = int(request.args.get('n', 15))
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    if handle is not None:
        try:
            handle = int(handle)
        except ValueError:
            return make_response('invalid handle', NOT_FOUND, headers)

    msg = data_manager.messages(handle=handle, start=start, end=end)
    result = stats.emojis(msg, n)

    return make_response('', NOT_IMPLEMENTED, headers)

# @app.route('/api/stats/sentiment', methods = ['GET'])
# @app.route('/api/stats/<handle>/sentiment', methods = ['GET'])
# def sentiment(handle=None):
#     start = request.args.get('start', None)
#     end = request.args.get('end', None)
#     if handle is not None:
#         try:
#             handle = int(handle)
#         except ValueError:
#             return make_response('invalid handle', NOT_FOUND, headers)
#
#     msg = data_manager.messages(handle=handle, start=start, end=end)
#     # result = stats.sentiment(msg)
#     senti.process(msg)
#
#     return make_response('', NOT_IMPLEMENTED, headers)

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
