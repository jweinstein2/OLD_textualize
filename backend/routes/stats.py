import src.stats.emoji as emoji_stats
import src.stats.sentiment as sentiment_stats
import src.stats.language as language_stats
import src.stats.general as general_stats

from flask import request, jsonify, make_response
from . import routes

import src.data_manager as data_manager

headers = {"Content-Type": "application/json"}
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
NOT_FOUND = 404
SERVER_ERROR = 500
NOT_IMPLEMENTED = 501

@routes.route('/stats/summary', methods = ['GET'])
def summary():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(start=start, end=end)
    result = general_stats.summary(msg)
    return make_response(result, OK, headers)

@routes.route('/stats/frequency', methods = ['GET'])
@routes.route('/stats/<number>/frequency', methods = ['GET'])
def frequency(number=None):
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    period = request.args.get('period', 'M')

    msg = data_manager.messages(number=number, start=start, end=end)
    result = general_stats.frequency(msg, period=period)
    return make_response(result, OK, headers)


@routes.route('/stats/emoji', methods = ['GET'])
@routes.route('/stats/<number>/emoji', methods = ['GET'])
def emoji_summary(number=None):
    n = int(request.args.get('n', 5))
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(number=number, start=start, end=end)
    result = emoji_stats.contact_summary(msg, n)
    return make_response(result, OK, headers)

@routes.route('/stats/sentiment', methods = ['GET'])
@routes.route('/stats/<number>/sentiment', methods = ['GET'])
def sentiment_summary(number=None):
    n = int(request.args.get('n', 5))
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(number=number, start=start, end=end)
    result = sentiment_stats.sentiment(msg)
    return make_response(result, OK, headers)

# @routes.route('/stats/tapback', methods = ['GET'])
# @routes.route('/stats/<number>/tapback', methods = ['GET'])
# def tapback_summary(number=None):
#     n = int(request.args.get('n', 5))
#     start = request.args.get('start', None)
#     end = request.args.get('end', None)
#
#     msg = data_manager.messages(number=number, start=start, end=end)
#     result = stats.tapback(msg)
#     return make_response(result, OK, headers)

@routes.route('/stats/<number>/language', methods =['GET'])
def diction_summary(number):
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    msg = data_manager.messages(number=number, start=start, end=end)
    result = language_stats.contact_summary(msg)
    return make_response(result, OK, headers)

