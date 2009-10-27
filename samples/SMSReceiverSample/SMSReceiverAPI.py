# -*- coding: cp1252 -*-
# SMSReceiver API.
#
# Features:
# * Class Implementation to receive SMS messages via mail server.


import quopri # quoted printable emails
import poplib # simple pop3 handling

class SMSReceiver:
    def ReadSMS(self, msg):
        """Gets an SMS message inside an email message."""

        for i in range(len(msg)):
            # Read Content-Type and encoding
            if msg[i].startswith('Content-Type:'):
                try:
                    ctype, encoding = map(str.strip, msg[i].split(':')[1].split(';'))
                    encoding = encoding.split('=')[1].strip()
                except:
                    encoding = 'ascii'
            # Find end of headers (blank line)
            if not msg[i]:
                break

        #body
        body=msg[i+1:]
        # first match
        number = body[0].split(':',1)
        if len(number)>1:
            number = number[1]
            message = body[1].split(':',1)
            if len(message)>1:
                message = unicode(quopri.decodestring(message[1]),'utf8')
            return number, message
        else:
            return None # not an SMS

    def GetSMSList(self, server, user, pwd):

        print 'Connecting...'
        M = poplib.POP3(server)
        print 'Set user'
        M.user(user)
        print 'Set password'
        M.pass_(pwd)

        print 'Getting list...'

        SMSList = []
        
        for mid, length in [i.split() for i in M.list()[1]]:
            mid = int(mid)
            length = int(length)
            ret, msg, size = M.retr(mid)
            msgList = self.ReadSMS(msg)

            if msgList <> None:
                SMSList.append(msgList)
            
        return SMSList
