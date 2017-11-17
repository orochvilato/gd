from gd import app,use_cache,mdb
from flask import request,current_app,make_response
from gd.tools import json_response,cache_function
import re
import datetime

from gd.config import cache_pages_delay

@app.route('/logs')
def logs():
    resp = make_response(app.send_static_file('logs.html'))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp

@app.route('/updatelogs')
def updatelogs():
    return json_response(list(mdb.logs.find()))
