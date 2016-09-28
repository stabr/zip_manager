import os
import sys
import json

def config(key):
    value = ''
    data_file = os.path.dirname(__file__)+'/data.json'
    if os.path.exists(data_file):
        try:
                    value = json.load(open(data_file))[key]
        except Exception, e:
                    value = e
    # sys.platform
    return value
