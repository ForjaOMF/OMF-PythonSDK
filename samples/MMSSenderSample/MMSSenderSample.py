# -*- coding: cp1252 -*-
import httplib, urllib, urlparse

import MMSSenderAPI

mms=MMSSenderAPI.MMSSender()

log='6xxxxxxxx' # MSISDN
passw='xxxxxx' # User's password
user = mms.Login(log, passw)

if user == None :
    print 'Login error'
else :
    imgPath='c:\\cosas\\dibujo.jpg'
    mms.InsertImage(imgPath)

    #sndName='audio'
    #sndPath='c:\\cosas\\queen.mid'
    #mms.InsertAudio(sndName, sndPath)

    #vidName='video'
    #vidPath='c:\\videos\\vid.avi'
    #mms.InsertVideo(vidName, vidPath)

    dest='6xxxxxxxx' # message destination (can be email address)
    subject='subject' # message subject
    msg='message text' # message text
    response = mms.SendMessage(subject, dest, msg)
    if response.find('Tu mensaje ha sido enviado'):
        print "Message sent"

    mms.Logout()
