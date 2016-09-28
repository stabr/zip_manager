# -*- coding: utf-8 -*-
'''

Author: Dmitry Stabrov
------------------------------
description: Sending Message To Slack
------------------------------
'''

import os
import getpass
import urllib
import urllib2
from pprint import pprint

import setup

def send(recipient, msg, link=''):
    url = setup.config('slack_url')
    image = setup.config('slack_img')
    username = 'Studio Service'
    # channel = '#general'
    # msg = '@username:Hey, Nika-Bolt! What a lovely hair!'

    user = getpass.getuser()
    comp = os.environ.get('COMPUTERNAME','no_nema_comp')
    mes = 'user: %s,  comp: %s\n%s'%(user, comp, msg)
    text = mes.encode('utf-8')
    channel = '@%s'%recipient if recipient else ''
    values = {
              'language':'json',
              'payload':'{"username":"%s","icon_url":"%s","text": "%s","channel":"%s"}'%(username, image, text, channel)}
    
    try:
        data = urllib.urlencode(values)
        req =  urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        resp = response.read()
        if not resp == 'ok':
                    pprint(resp)
    except Exception, e:
        print '>> send/slack/message exception: %s'% e

# send('', u'It`s me')