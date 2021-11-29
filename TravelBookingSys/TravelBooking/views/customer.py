# Create your views here.
import json
from datetime import datetime

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TravelBooking.forms import *
from TravelBooking.models import *


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])

# 预定FLIGHT, BUS, HOTEL
