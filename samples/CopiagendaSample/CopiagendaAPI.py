# -*- coding: cp1252 -*-
import httplib, urllib

class Copiagenda:

    def ParseResponse (self, code) :
        """Parses the text that contains the contacts (separate by \t)
            Entrada: Text string
            Retorna: Contact list or 0 in case of error"""

        Contacts =[]
        contactDelimiter = '"Title"'

        if code[:7]!= contactDelimiter :
            return 0
        index = code.find ('\n"')
        FieldDescrip=(code[1:index-2]).split('"\t"')
        code = code [index+1:]
    
        index = code.find ('\n"')
        while index!=-1 :
            contact = (code [1:index-2]).split('"\t"')
            Contacts.append (contact)
            code = code [index+1:]
            index = code.find ('\n"')
        else :
            index = code.find ('\n')
            contact = (code [1:index-2]).split('"\t"')
            Contacts.append (contact)

        return Contacts


    def RetrieveContacts (self, login, pwd) :
        """Performs contact list retrieval
            Entrada: login=String with user's telephone number
                     pwd=String with user's password
            Retorna: Contact list stored for the user or 0 in case of error"""

        ## Return list
        ContactList = []
    
        params = urllib.urlencode ({'TM_ACTION': 'LOGIN','TM_LOGIN':login, 'TM_PASSWORD':pwd})
        headers = {"Content-type":"application/x-www-form-urlencoded","Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive"}
        conn=httplib.HTTPSConnection("copiagenda.movistar.es")
        conn.request ("POST", "/cp/ps/Main/login/Agenda",params, headers)
        resp=conn.getresponse()
        print resp.status
        print resp.getheaders()

        ## We are redirected and we receive a cookie
        headresp=resp.getheaders()
        cookie=headresp[1][1]
        cookie = cookie.replace(" Path=/, "," ")
        cookie = cookie.replace("; Domain=.movistar.es; Path=/","+")
        cookie = cookie.rstrip('+')
        print cookie
        headers2 = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Host" : "copiagenda.movistar.es", "Connection" :  "Keep-Alive","Cookie" : cookie}
        conn2=httplib.HTTPSConnection("copiagenda.movistar.es")
        conn2.request ("GET", "/cp/ps/Main/login/Verificacion?d=movistar.es",None, headers2)
        resp2=conn2.getresponse()
        print resp2.status
        response= resp2.read()
        inic=response.find("name=\"password")
        inic=response.find("value=",inic)
        finic=response.find(">",inic)
        encodedPwd = response[inic+6:finic]
        print encodedPwd

        ## We have to re-authenticate with user data + cookie and we get a session token
        params3 = urllib.urlencode ({'password':encodedPwd, 'u': login, 'd':'movistar.es'})
        headers3 = {"Content-type":"application/x-www-form-urlencoded", "Accept-Encoding" : "gzip, deflate", "Host" : "copiagenda.movistar.es" , "Referer" : "https://copiagenda.movistar.es/cp/ps/Main/login/Verificacion?d=movistar.es", "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Accept-Language" : "es", "Cache-Control" : "no-cache", "Connection" :  "Keep-Alive", "Cookie" : cookie}
        conn3=httplib.HTTPSConnection("copiagenda.movistar.es")
        conn3.request ("POST", "/cp/ps/Main/login/Authenticate",params3, headers3)
        resp3=conn3.getresponse()
        print resp3.status
        token = resp3.read()
        initoken=token.find("&t=")
        endtoken=token.find("\"",initoken)
        token=token[initoken:endtoken]

        ## We request a list of contacts separate by tabs
        params4 = urllib.urlencode ({'fileFormat':'TEXT', 'charset': '8859_1', 'delimiter': 'TAB'})
        headers4 = {"Content-type":"application/x-www-form-urlencoded", "Accept-Encoding" : "gzip, deflate", "Host" : "copiagenda.movistar.es" , "Referer" : "https://copiagenda.movistar.es/cp/ps/Main/login/Verificacion?d=movistar.es", "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Accept-Language" : "es", "Cache-Control" : "no-cache", "Connection" :  "Keep-Alive", "Cookie" : cookie}
        conn4=httplib.HTTPSConnection("copiagenda.movistar.es")
        path4 = "/cp/ps/PSPab/preferences/ExportContacts?d=movistar.es&c=yes&u="+login+token
        conn4.request ("POST", path4 ,params4, headers4)
        resp4=conn4.getresponse()
        HTMLCod=resp4.read()
        print HTMLCod
        ContactList=self.ParseResponse(HTMLCod)
        
        conn4.close()
        conn3.close()
        conn2.close()
        conn.close()
        return ContactList

    def SearchByName (self, name, addressBook):
        """Function to search for a contact by its name
            Entrada: name=string with contact name or part of it
                     addressBook=contact list to search in
            Retorna: full contact with all its fields"""

        ## Searching
        for n in addressBook :
            if name in n[3] :
                return n
        return 0
