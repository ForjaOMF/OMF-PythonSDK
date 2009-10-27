# -*- coding: cp1252 -*-
import httplib, urllib

import CopiagendaAPI

log='6xxxxxxxx' # MSISDN
passw='xxxxxx' # password to access copiagenda web

copia = CopiagendaAPI.Copiagenda()

MyAddressBook = copia.RetrieveContacts (log,passw)
contact = copia.SearchByName ('name',MyAddressBook) # Warning! it's case sensitive
if contact==0 :
    print "Contact not found"
else :
    print contact[3]+" "+contact[11] # Maybe telephone number is not field number 11 but any other one
