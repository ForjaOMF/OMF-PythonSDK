# -*- coding: cp1252 -*-
import httplib, urllib
import xml.parsers.expat

import time

class ContactsParser :
    """Class to parse XML received when you request contact list"""

    Contacts = {}
    bNickName = 0
    bName = 0
    bUserID = 0

    name = ""
    userId = ""

    def start_elementContact(self,name,attrs):
        """Called automatically when an XML element is open
            Input: name=element name
                     attrs: element attributes"""
        
        if name == 'NickName' :
            self.bNickName = 1
            self.bUserID = 0
            self.bName = 0
        elif self.bNickName and name == 'Name' :
            self.bUserID = 0
            self.bName = 1
        elif self.bNickName and name == 'UserID' :
            self.bUserID = 1
            self.bName = 0

    def end_elementContact(self,name):
        """Called automatically when an XML element is read
            Input: name=element name"""
        
        if name == 'NickName' :
            self.Contacts[self.userId]=self.name
            self.bNickName = 0
            self.bUserID = 0
            self.bName = 0
            
    def char_dataContact(self,data):
        """Called automatically when an XML element is closed
            Input: data=element data"""
        
        if self.bName == 1 :
            self.name = str(data)
        elif self.bUserID == 1 :
            self.userId = str(data)

    def GetContactList(self, response) :
        """Gets contact list
            Input: response=string with XML data received from server
            Returns: contact list"""
        
        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.start_elementContact
        p.EndElementHandler = self.end_elementContact
        p.CharacterDataHandler = self.char_dataContact

        p.Parse(response)

        return self.Contacts

class PresenceParser :
    """Class to parse XML received when you receive a presence update"""

    Presents = {}
    bPresence = 0
    bUserID = 0
    bUserAvailability = 0
    bValue = 0
    bAlias = 0
    bAliasValue = 0

    userId = ''
    nickName = ''
    value = ''

    def start_elementPresence(self,name,attrs):
        """Called automatically when an XML element is open
            Input: name=element name
                     attrs: element attributes"""

        if name == 'Presence' :
            self.bPresence = 1
            self.bUserID = 0
            self.bUserAvailability = 0
            self.bValue = 0
            self.bAlias = 0
            self.bAliasValue = 0
        elif self.bPresence == 1 and name == 'OnlineStatus' :
            self.bUserID = 0
            self.bUserAvailability = 1
            self.bValue = 0
            self.bAlias = 0
            self.bAliasValue = 0
        elif self.bPresence == 1 and name == 'Alias' :
            self.bUserID = 0
            self.bUserAvailability = 0
            self.bValue = 0
            self.bAlias = 1
            self.bAliasValue = 0
        elif self.bPresence == 1 and name == 'UserID' :
            self.bUserID = 1
            self.bUserAvailability = 0
            self.bValue = 0
            self.bAlias = 0
            self.bAliasValue = 0
        elif self.bUserAvailability == 1 and name == 'PresenceValue' :
            self.bValue = 1
            self.bAliasValue = 0
        elif self.bAlias == 1 and name == 'PresenceValue' :
            self.bValue = 0
            self.bAliasValue = 1

    def end_elementPresence(self,name):
        """Called automatically when an XML element is closed
            Input: name=element name"""

        if name == 'Presence' :
            self.Presents[self.userId]=[self.value,self.nickName]
            self.bPresence = 0
            self.bUserID = 0
            self.bUserAvailability = 0
            self.bValue = 0
            self.bAlias = 0
            self.bAliasValue = 0
        elif name == 'OnlineStatus' :
            self.bUserAvailability = 0
            self.bValue = 0
        elif name == 'Alias' :
            self.bAlias = 0
            self.bAliasValue = 0
        elif name == 'UserID' :
            self.bUserID = 0
        elif name == 'PresenceValue' :
            self.bValue = 0
            self.bAliasValue = 0
            
    def char_dataPresence(self,data):
        """Called automatically when an XML element is read
            Input: data=element data"""

        if self.bUserID == 1 :
            self.userId = str(data)
        elif self.bValue == 1 :
            self.value = str(data)
        elif self.bAliasValue == 1 :
            self.nickName = str(data)

    def GetPresentsList(self, response) :
        """Gets presence list
            Input: response=string with XML data received from server
            Returns: contact list"""

        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.start_elementPresence
        p.EndElementHandler = self.end_elementPresence
        p.CharacterDataHandler = self.char_dataPresence

        p.Parse(response)

        return self.Presents

class MessageParser :
    """Class to parse XML received when you receive a new message"""

    bNewMessage = 0
    bSender = 0
    bUserID = 0
    bContentData = 0

    userId = ''
    message = ''

    def start_elementMessage(self,name,attrs):
        """Called automatically when an XML element is open
            Input: name=element name
                     attrs: element attributes"""

        if name == 'NewMessage' :
            self.bNewMessage = 1
            self.bSender = 0
            self.bUserID = 0
            self.bContentData = 0
        elif self.bNewMessage == 1 and name == 'Sender' :
            self.bSender = 1
            self.bUserID = 0
            self.bContentData = 0
        elif self.bNewMessage == 1 and name == 'ContentData' :
            self.bSender = 0
            self.bUserID = 0
            self.bContentData = 1
        elif self.bSender == 1 and name == 'UserID' :
            self.bUserID = 1

    def end_elementMessage(self,name):
        """Called automatically when an XML element is closed
            Input: name=element name"""

        if name == 'NewMessage' :
            self.bNewMessage = 0
            self.bSender = 0
            self.bUserID = 0
            self.bContentData = 0
        elif name == 'Sender' :
            self.bSender = 0
            self.bUserID = 0
        elif name == 'UserID' :
            self.bSender = 0
            self.bUserID = 0
        elif name == 'ContentData' :
            self.bContentData = 0
            
    def char_dataMessage(self,data):
        """Called automatically when an XML element is read
            Input: data=element data"""

        if self.bUserID == 1 :
            self.userId = str(data)
        elif self.bContentData == 1 :
            self.message = self.message + unicode(data)

    def GetMessage(self, response) :
        """Gets received message text
            Input: response=string with XML data received from server
            Returns: sender user ID | message text"""

        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.start_elementMessage
        p.EndElementHandler = self.end_elementMessage
        p.CharacterDataHandler = self.char_dataMessage

        p.Parse(response)

        return self.userId+'|'+self.message

class AuthRequestParser :
    """Class to parse XML received when a contact requests authorization to be informed about your presenc status"""

    bPresence = 0
    bUserID = 0
    bTransactionID = 0

    userId = ""
    transactionId = ""

    def start_elementContact(self,name,attrs):
        """Called automatically when an XML element is open
            Input: name=element name
                     attrs: element attributes"""

        if name == 'PresenceAuth-Request' :
            self.bTransactionID = 0
            self.bPresence = 1
            self.bUserID = 0
        elif self.bPresence and name == 'UserID' :
            self.bUserID = 1
        elif name == 'TransactionID' :
            self.bTransactionID = 1
            self.bPresence = 0
            self.bUserID = 0

    def end_elementContact(self,name):
        """Called automatically when an XML element is closed
            Input: name=element name"""

        if name == 'PresenceAuth-Request' :
            self.bPresence = 0
            self.bUserID = 0
        elif name == 'UserID' :
            self.bUserID = 0
        elif name == 'TransactionID' :
            self.bTransactionID = 0
            
    def char_dataContact(self,data):
        """Called automatically when an XML element is read
            Input: data=element data"""

        if self.bUserID == 1 :
            self.userId = str(data)
        if self.bTransactionID == 1 :
            self.transactionId = str(data)

    def GetUser(self, response) :
        """Gets userId and transaction id
            Input: response=string with XML data received from server
            Returns: contact user ID | transaction id"""
        
        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.start_elementContact
        p.EndElementHandler = self.end_elementContact
        p.CharacterDataHandler = self.char_dataContact

        p.Parse(response)

        return self.userId+'|'+self.transactionId

class SMS20 :

    sessionID = ""
    nTransId = 1
    
    bSessionID = 0
    myAlias = ''
    
    def Login(self, log, passw) :
        """Performs login to movistar web
            Entrada: login=string with user's telephone number
                      passw=string with user's password
            Retorna: Session Id"""

        ## Start login
        params = urllib.urlencode ({'TM_ACTION':'AUTHENTICATE', 'TM_LOGIN':log, 'TM_PASSWORD':passw, 'SessionCookie':'ColibriaIMPS_367918656', 'ClientID':'WV:InstantMessenger-1.0.2309.16485@COLIBRIA.PC-CLIENT'})
        headers = {"Content-type":"application/x-www-form-urlencoded"}
        conn=httplib.HTTPConnection("impw.movistar.es")
        conn.request ("POST", "/tmelogin/tmelogin.jsp",params, headers)
        resp=conn.getresponse()
        response=resp.read()

        conn.close()

        session = self.GetSessionID(response)
        print session
        return session


    def start_elementSession(self,name, attrs):
        """Called automatically when an XML element is open
            Input: name=element name
                     attrs: element attributes"""

        if name == 'SessionID' :
            self.bSessionID = 1
            
    def end_elementSession(self,name):
        """Called automatically when an XML element is closed
            Input: name=element name"""

        if name == 'SessionID' :
            self.bSessionID = 0
            
    def char_dataSession(self,data):
        """Called automatically when an XML element is read
            Input: data=element data"""

        if self.bSessionID == 1 :
            self.sessionID = data

    def GetSessionID(self, text) :
        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.start_elementSession
        p.EndElementHandler = self.end_elementSession
        p.CharacterDataHandler = self.char_dataSession

        p.Parse(text)

        return self.sessionID

    def Connect(self, log, nickname) :
        """Connects to SMS2.0 service
            Input: log=string with telephone number
                      nickname=cadena con el nickname que queramos utilizar (sólo es necesario la primera vez)
            Returns: Contact list of the given telephone number"""

        # Send <ClientCapability-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>1</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ClientCapability-Request><ClientID><URL>WV:InstantMessenger-1.0.2309.16485@COLIBRIA.PC-CLIENT</URL></ClientID><CapabilityList><ClientType>COMPUTER</ClientType><InitialDeliveryMethod>P</InitialDeliveryMethod><AcceptedContentType>text/plain</AcceptedContentType><AcceptedContentType>text/html</AcceptedContentType><AcceptedContentType>image/png</AcceptedContentType><AcceptedContentType>image/jpeg</AcceptedContentType><AcceptedContentType>image/gif</AcceptedContentType><AcceptedContentType>audio/x-wav</AcceptedContentType><AcceptedContentType>image/jpg</AcceptedContentType><AcceptedTransferEncoding>BASE64</AcceptedTransferEncoding><AcceptedContentLength>256000</AcceptedContentLength><MultiTrans>1</MultiTrans><ParserSize>300000</ParserSize><SupportedCIRMethod>STCP</SupportedCIRMethod><ColibriaExtensions>T</ColibriaExtensions></CapabilityList></ClientCapability-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <Service-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>2</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><Service-Request><ClientID><URL>WV:InstantMessenger-1.0.2309.16485@COLIBRIA.PC-CLIENT</URL></ClientID><Functions><WVCSPFeat><FundamentalFeat /><PresenceFeat /><IMFeat /><GroupFeat /></WVCSPFeat></Functions><AllFunctionsRequest>T</AllFunctionsRequest></Service-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <UpdatePresence-Request> to inform that you are online
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>3</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><UpdatePresence-Request><PresenceSubList xmlns="http://www.openmobilealliance.org/DTD/WV-PA1.2"><OnlineStatus><Qualifier>T</Qualifier></OnlineStatus><ClientInfo><Qualifier>T</Qualifier><ClientType>COMPUTER</ClientType><ClientTypeDetail xmlns="http://imps.colibria.com/PA-ext-1.2">PC</ClientTypeDetail><ClientProducer>Colibria As</ClientProducer><Model>TELEFONICA Messenger</Model><ClientVersion>1.0.2309.16485</ClientVersion></ClientInfo><CommCap><Qualifier>T</Qualifier><CommC><Cap>IM</Cap><Status>OPEN</Status></CommC></CommCap><UserAvailability><Qualifier>T</Qualifier><PresenceValue>AVAILABLE</PresenceValue></UserAvailability></PresenceSubList></UpdatePresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <GetList-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>4</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><GetList-Request /></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <GetPresence-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>5</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><GetPresence-Request><User><UserID>wv:"""+log+"""@movistar.es</UserID></User></GetPresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()
        pp0=PresenceParser()
        listI=pp0.GetPresentsList(response)
        myStatus = listI['wv:' + log + '@movistar.es']
        self.myAlias = myStatus[1]

        # Send <ListManage-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>6</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ListManage-Request><ContactList>wv:"""+log+"""/~pep1.0_privatelist@movistar.es</ContactList><ReceiveList>T</ReceiveList></ListManage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        cp=ContactsParser()
        RetList=cp.GetContactList(response)

        # Send <CreateList-Request>
        nickList = ''
        if RetList != {} :
            nickList = '<NickList>'
            for k,v in RetList.iteritems() :
                nickList = nickList + '<NickName><Name>%s</Name><UserID>%s</UserID></NickName>' % (v, k)
            nickList = nickList + '</NickList>'
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>7</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><CreateList-Request><ContactList>wv:"""+log+"""/~PEP1.0_subscriptions@movistar.es</ContactList>"""+nickList+"""</CreateList-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <SubscribePresence-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>8</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><SubscribePresence-Request><ContactList>wv:"""+log+"""/~PEP1.0_subscriptions@movistar.es</ContactList><PresenceSubList xmlns="http://www.openmobilealliance.org/DTD/WV-PA1.2"><OnlineStatus /><ClientInfo /><FreeTextLocation /><CommCap /><UserAvailability /><StatusText /><StatusMood /><Alias /><StatusContent /><ContactInfo /></PresenceSubList><AutoSubscribe>T</AutoSubscribe></SubscribePresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <UpdatePresence-Request> to give your nick
        # Only first time or when you want to change your nickname
        if nickname != '' :
            params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>9</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><UpdatePresence-Request><PresenceSubList xmlns="http://www.openmobilealliance.org/DTD/WV-PA1.2"><Alias><Qualifier>T</Qualifier><PresenceValue>"""+nickname+"""</PresenceValue></Alias></PresenceSubList></UpdatePresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
            headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
            conn=httplib.HTTPConnection("sms20.movistar.es")
            conn.request ("POST", "/", params, headers)
            resp=conn.getresponse()

            self.myAlias = nickname

        conn.close()

        self.nTransId = 10

        return RetList

    def Polling(self) :
        """Polling to receive async notifications
            Input: none
            Returns: Response text"""

        # Send <Polling-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID /></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><Polling-Request /></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        conn.close()
        
        return response

    def AddContact(self, log, contact) :
        """Adds a contact to your list
            Input: log=string with your telephone number
                     contact=string with contact telephone number
            Returns: List of present contacts"""

        RetList = {}

        # Send <Search-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><Search-Request><SearchPairList><SearchElement>USER_MOBILE_NUMBER</SearchElement><SearchString>"""+contact+"""</SearchString></SearchPairList><SearchLimit>50</SearchLimit></Search-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <GetPresence-Request> to get contact presence status
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+1)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><GetPresence-Request><User><UserID>wv:"""+contact+"""@movistar.es</UserID></User><PresenceSubList xmlns="http://www.openmobilealliance.org/DTD/WV-PA1.2"><OnlineStatus /><ClientInfo /><GeoLocation /><FreeTextLocation /><CommCap /><UserAvailability /><StatusText /><StatusMood /><Alias /><StatusContent /><ContactInfo /></PresenceSubList></GetPresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        cp=PresenceParser()
        RetList=cp.GetPresentsList(response)

        nickname=RetList['wv:'+contact+'@movistar.es'][1]

        # Send <ListManage-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+2)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ListManage-Request><ContactList>wv:"""+log+"""/~PEP1.0_subscriptions@movistar.es</ContactList><AddNickList><NickName><Name>"""+nickname+"""</Name><UserID>wv:"""+contact+"""@movistar.es</UserID></NickName></AddNickList><ReceiveList>T</ReceiveList></ListManage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <ListManage-Request> esta vez para la PrivateList
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+3)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ListManage-Request><ContactList>wv:"""+log+"""/~PEP1.0_privatelist@movistar.es</ContactList><AddNickList><NickName><Name>"""+nickname+"""</Name><UserID>wv:"""+contact+"""@movistar.es</UserID></NickName></AddNickList><ReceiveList>T</ReceiveList></ListManage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        self.nTransId = self.nTransId + 4

        conn.close()

        return RetList

    def AuthorizeContact(self, user, transaction) :
        """Authorizes a contact to know your presence status
            Input: user=contact's user Id (wv:6xxxxxxxx@movistar.es)
                     transaction=transaction id received in the authorization request
            Returns: void"""
        
        # Send <GetPresence-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><GetPresence-Request><User><UserID>"""+user+"""</UserID></User><PresenceSubList xmlns="http://www.openmobilealliance.org/DTD/WV-PA1.2"><OnlineStatus /><ClientInfo /><GeoLocation /><FreeTextLocation /><CommCap /><UserAvailability /><StatusText /><StatusMood /><Alias /><StatusContent /><ContactInfo /></PresenceSubList></GetPresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <Status> para hacer el ack de la petición
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Response</TransactionMode><TransactionID>"""+transaction+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><Status><Result><Code>200</Code></Result></Status></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <PresenceAuth-User>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+1)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><PresenceAuth-User><UserID>"""+user+"""</UserID><Acceptance>T</Acceptance></PresenceAuth-User></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        self.nTransId = self.nTransId + 2
        
        conn.close()

    def DeleteContact(self, log, contact) :
        """Deletes a contact from your list
            Input: log=string with your user telephone number
                     contact=user id of the contact to delete (wv:6xxxxxxxx@movistar.es)
            Returns: void"""

        # Send <ListManage-Request> to delete contact from subscription list
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ListManage-Request><ContactList>wv:"""+log+"""/~PEP1.0_subscriptions@movistar.es</ContactList><RemoveNickList><UserID>"""+contact+"""</UserID></RemoveNickList><ReceiveList>T</ReceiveList></ListManage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <ListManage-Request> to delete contact from private list
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+1)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><ListManage-Request><ContactList>wv:"""+log+"""/~PEP1.0_privatelist@movistar.es</ContactList><RemoveNickList><UserID>"""+contact+"""</UserID></RemoveNickList><ReceiveList>T</ReceiveList></ListManage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <UnsubscribePresence-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+2)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><UnsubscribePresence-Request><User><UserID>"""+contact+"""</UserID></User></UnsubscribePresence-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <DeleteAttributeList-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+3)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><DeleteAttributeList-Request><UserID>"""+contact+"""</UserID><DefaultList>F</DefaultList></DeleteAttributeList-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        # Send <CancelAuth-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId+4)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><CancelAuth-Request><UserID>"""+contact+"""</UserID></CancelAuth-Request></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        self.nTransId = self.nTransId + 5

        conn.close()

    def SendMessage(self, log, destination, message) :
        """Sends a message to destination number
            Input: log=string with your telephone number
                     destination=string with destination user id (wv:6xxxxxxxx@movistar.es)
                     message=message text
            Returns: void"""

        # Send <SendMessage-Request>
        paramsMsg = '<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>'+self.sessionID.encode('utf8')+'</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>'+str(self.nTransId)+'</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><SendMessage-Request><DeliveryReport>F</DeliveryReport><MessageInfo><ContentType>text/html</ContentType><ContentSize>148</ContentSize><Recipient><User><UserID>'+destination+'</UserID></User></Recipient><Sender><User><UserID>'+log+'@movistar.es</UserID></User></Sender></MessageInfo><ContentData>&lt;span style="color:#000000;font-family:"Microsoft Sans Serif";font-style:normal;font-weight:normal;font-size:12px;"&gt;'+message+'&lt;/span&gt;</ContentData></SendMessage-Request></TransactionContent></Transaction></Session></WV-CSP-Message>'
        
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", paramsMsg, headers)
        resp=conn.getresponse()
        response=resp.read()

        self.nTransId = self.nTransId + 1

        conn.close()

    def Disconnect(self) :
        """Disconnects from SMS2.0 service
            Input: none
            Returns: void"""

        # Send <Logout-Request>
        params = """<?xml version="1.0" encoding="utf-8"?><WV-CSP-Message xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.openmobilealliance.org/DTD/WV-CSP1.2"><Session><SessionDescriptor><SessionType>Inband</SessionType><SessionID>"""+self.sessionID+"""</SessionID></SessionDescriptor><Transaction><TransactionDescriptor><TransactionMode>Request</TransactionMode><TransactionID>"""+str(self.nTransId)+"""</TransactionID></TransactionDescriptor><TransactionContent xmlns="http://www.openmobilealliance.org/DTD/WV-TRC1.2"><Logout-Request /></TransactionContent></Transaction></Session></WV-CSP-Message>"""
        headers = {'Content-type':'application/vnd.wv.csp.xml', 'Expect':'100-continue'}
        conn=httplib.HTTPConnection("sms20.movistar.es")
        conn.request ("POST", "/", params, headers)
        resp=conn.getresponse()
        response=resp.read()

        self.nTransId =  1

        conn.close()

