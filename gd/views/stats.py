# -*- coding: utf-8 -*-

from gd import app,use_cache,mdb
from flask import request,render_template
from gd.tools import json_response,cache_function
from bson import json_util
import re
import random
import datetime

@app.route('/stats/tops')
@cache_function(expires=120)
def tops():
    pcts={'gauche':[],'droite':[],'passur':[]}
    for c in mdb.clivages.find():
        total = c['g']+c['d']
        if total>0:
            pctg = round(100*float(c['g'])/total,0)
            pctd = 100-pctg
            passur = abs(pctg-50)
            if abs(pctg-50)<2:
                pcts['passur'].append((c['n'],passur,pctg,pctd))
            pcts['gauche'].append((c['n'],pctg))
            pcts['droite'].append((c['n'],pctd))

    pcts['passur'].sort(key=lambda x:x[1])
    pcts['gauche'].sort(key=lambda x:x[1],reverse=True)
    pcts['droite'].sort(key=lambda x:x[1],reverse=True)
    return render_template('tops.html',g=pcts['gauche'][:10],d=pcts['droite'][:10],ps=pcts['passur'])
