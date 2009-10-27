# -*- coding: cp1252 -*-
import httplib, urllib

#import SMSSenderAPI
import LocalizameAPI


##---------------------------------------------------------------------------------------------
## Cuerpo principal

locator='686013749' # MSISDN
passwSMS='xxxxxx' # password to send SMS messages
passw='18288'
# Telephone Number to locate (we have to be allowed)
locatable='686013749' # MSISDN
passwSMS2='xxxxxx' # password to send SMS messages
passw2='18288' # password to access Localízame service.

"""It has to be done from our terminal by now"""
# Obtain locator and locatable passwords
#sender = SMSSenderAPI.SMSSender()
#sender.SendMessage(locatable, passwSMS2, '424', 'CLAVE')
#sender.SendMessage(locator, passwSMS, '424', 'CLAVE')

# locatable authorizes locator
loc1 = LocalizameAPI.Localizame()
loc1.Login(locatable, passw2)
loc1.Authorize(locator)
loc1.Logout()

# Starting location
loc2 = LocalizameAPI.Localizame()
loc2.Login(locator, passw)
print loc2.Locate(locatable)
loc2.Logout()

# locatable unauthorizes locator
loc3 = LocalizameAPI.Localizame()
loc3.Login(locatable, passw2)
loc3.Unauthorize(locator)
loc3.Logout()

