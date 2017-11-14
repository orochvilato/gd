
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
import pymongo
from bson import json_util

from config_private import mongo_readwrite_user,mongo_readwrite_password

client = pymongo.MongoClient('mongodb://%s:%s@gauchedroite.orvdev.fr:27017/gauchedroite' %(mongo_readwrite_user,mongo_readwrite_password))
mdb = client.gauchedroite

from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import bmemcached
memcache = bmemcached.Client(('memcache.orvdev.fr:11211',))

def use_cache(k,fct,expires=60):
    if expires==0:
        memcache.delete(k)
        v=None
    else:
        v = memcache.get(k)
    if not v:
        v = fct()
        memcache.set(k,v,time=expires)
    else:
        pass
    return v

from views import api,stats
