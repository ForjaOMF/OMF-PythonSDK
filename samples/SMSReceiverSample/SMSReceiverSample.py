# -*- coding: cp1252 -*-
# SMSReceiver sample code
#

import SMSReceiverAPI

server = 'mailserver.com'
user = 'user'
pwd = 'password'

receiver = SMSReceiverAPI.SMSReceiver()
SMSList = receiver.GetSMSList(server, user, pwd)
print SMSList
