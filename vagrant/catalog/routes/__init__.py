from flask import Blueprint
routes = Blueprint('routes', __name__)

from .departments import *
from .loginprovider import *
from .seminars import *
