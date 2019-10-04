from flask import Blueprint
routes = Blueprint('routes', __name__)

from .data import *
from .stats import *
from .basic import *
