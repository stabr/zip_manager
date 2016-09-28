import os
import json

def config(key):
    value = "\nCan`t get any data file!\n"
    data = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data.json'))
    if os.path.exists(data):
                try:
                    value = json.load(open(data))[key]
                except Exception, e:
                    value = e
    return value
