# -*- coding: utf-8 -*-

from gd import app,use_cache,mdb
from flask import request
from gd.tools import json_response,cache_function
from bson import json_util
import re
import random
import datetime
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

from gd.config import cache_pages_delay

VERSIONS_AUTORISEES = {'ios':['1.1'],
                       'android':['1.5']}


@app.route('/api/clivages/get',methods=['GET'])
@cache_function(expires=cache_pages_delay)
def getclivages():
    resp = {'data':list(mdb.clivages.find({},{'_id':None,'i':1,'d':1,'g':1,'n':1}))}
    return json_response(resp)

@app.route('/api/clivages/update',methods=['POST','PUT'])
def updateclivages():
    resp = request.get_json(force=True,silent=True)
    ops = []
    user_agent = request.headers.get('User-Agent')
    archi = 'ios' if ('CFNetwork' in user_agent and 'Darwin' in user_agent) else 'android'
    if 1:
        mdb.logs.insert_one({'archi':archi,'timestamp':datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),'data':resp,'ip':request.environ['REMOTE_ADDR'],'user_agent':request.headers.get('User-Agent')})
    if resp and resp.get('version')=='dev':
        return '',403

    if not resp or not resp.get('version') in VERSIONS_AUTORISEES[archi]:
        return '',403

    #return '',200

    for o in resp['data']:
        if o.get('g',False):
            ops.append(UpdateOne({'i':o['i']},{'$inc':{'g':1}}))
        else:
            ops.append(UpdateOne({'i':o['i']},{'$inc':{'d':1}}))
    if len(ops)>0:
        mdb.clivages.bulk_write(ops)
    return '',200

@app.route('/api/clivages/init',methods=['get'])
def init():
    return "desactivé"
    resp = json_util.loads(open('gd/data.json').read())
    mdb.clivages.remove()
    mdb.clivages.insert_many(resp)
    return json_response(resp)
