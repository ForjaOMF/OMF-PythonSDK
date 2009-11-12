# -*- coding: cp1252 -*-
# AutoWP sample code
#

import httplib, urllib

import AutoWPAPI

login = '6xxxxxxxx'
pwd = 'xxxxxx'

url = 'http://www.google.com'
text = 'Google'

sender = AutoWPAPI.AutoWP()
sender.SendAutoWP(login, pwd, url, text)
