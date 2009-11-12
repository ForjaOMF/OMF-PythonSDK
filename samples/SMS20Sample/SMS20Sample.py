# -*- coding: cp1252 -*-
import httplib, urllib
import xml.parsers.expat

import time

import SMS20API

##---------------------------------------------------------------------------------------------
## Main program

sms20 = SMS20API.SMS20()

log='6xxxxxxxx' # MSISDN
passw='xxxxxx' # password to SMS2.0 service

contact='6yyyyyyyy' # telephone number to add contact

session = sms20.Login(log,passw)
sms20.Connect(log,'')

contactList = {}
contactList = sms20.AddContact(log, contact)
print contactList

message = ''
# Polling until we receive " bye"
while message != ' bye' :
    response=sms20.Polling()

    pp=SMS20API.PresenceParser()
    plist=pp.GetPresentsList(response)
    if plist != {} :
        for n in plist :
            if n != 'wv:'+log+'@movistar.es' :
                if plist[n][0] == 'T' :
                    print plist[n][1] + '(' + n+ ') is ONLINE'
                else : 
                    print plist[n][1] + '(' + n+ ') is OFFLINE'
            

    mp=SMS20API.MessageParser()
    text=mp.GetMessage(response)
    parts = text.split('|')
    if len(parts) >0 :
        Sender = parts[0]
        if len(parts) > 1 :
            msgFormat = parts[1]
            partsFormat = msgFormat.split('<')
            if len(partsFormat) > 1 :
                tailFormat = partsFormat[1]
                tailParts = tailFormat.split('>')
                if len(tailParts) > 1 :
                    messageText = tailParts[1]
                    message = messageText
                    messageText2 = messageText.encode('latin_1')
                    print str(Sender) + ': "' + messageText2 + '"'
                    # Send the same message appending " to you too"
                    
                    messageText = messageText.encode('latin_1')
                    messageText = messageText + ' to you too'
                    
                    messageText = unicode(messageText,'latin-1')
                    messageText = messageText.encode('utf8')

                    sms20.SendMessage(log.encode('utf8'),Sender.encode('utf8'),messageText)

    # Ask authorization request
    arp=SMS20API.AuthRequestParser()
    userANDtransaction=arp.GetUser(response)
    userANDtransactionList=userANDtransaction.split('|')
    user=userANDtransactionList[0]
    transaction=userANDtransactionList[1]
    if user != '' :
        # ToDo: Ask whether authorize the contact or not
        sms20.AuthorizeContact(user, transaction)

    time.sleep(3)

sms20.DeleteContact(log, contact)

sms20.Disconnect()
