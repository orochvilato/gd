# -*- coding: utf-8 -*-

from gd import app,use_cache,mdb
from flask import request
from gd.tools import json_response,cache_function
import re
import random
import datetime

from gd.config import cache_pages_delay


@app.route('/api/get')
@cache_function(expires=cache_pages_delay)
def getclivages():
    resp = mdb.clivages.find()
    return json_response(list(resp))
