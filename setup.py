import os
import json

def config(key):
    value = "\nCan`t get any data file!\n"
    data = os.path.abspath(os.path.join(os.path.dirname(__file__),'data.json')).replace('\\', '/')
    if os.path.exists(data):
        try:
            value = json.load(open(data))[key]
        except Exception, e:
            value = str(e)
    return value