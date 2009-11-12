# -*- coding: cp1252 -*-
import httplib, urllib

class Localizame :

    cookie = ''
    
    def Login (self, login, pwd) :
        """Performs login to the server
            Input: login=String with user's telephone number
                      pwd=String with user's password"""

        print "Login"
        params = urllib.urlencode ({'usuario':login, 'clave':pwd, 'submit.x': '36', 'submit.y': '6'})
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive"}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("POST", "/login.do",params, headers)
        resp=conn.getresponse()

        cookie = ''
        headresp=resp.getheaders()
        for n in headresp :
            if n[0] == 'set-cookie' :
                    cookie = n[1]

        cookieList = cookie.split(';')
        cookie = cookieList[0]  # We use only the first part of the list
        self.cookie = cookie

        # We have to access this page or we will not be allowed to authorize any user.
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie, 'Referer': 'http://www.localizame.movistar.es/login.do'}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("GET", "/nuevousuario.do", None, headers)
        resp=conn.getresponse()

        conn.close()

    def Locate (self, number) :
        """Performs location search of a user
            Input: number=String with user's telephone number"""

        print "Locating..."
        params = urllib.urlencode ({'telefono':number})
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("POST", "/buscar.do",params, headers)
        resp=conn.getresponse()
        response=resp.read()

        txtlist = response.partition(number)
        endText = txtlist[2].partition('metros.')
        conn.close()

        return txtlist[1] + endText[0] + endText[1]

    def Authorize (self, number) :
        """Authorizes another user to locate us
            Input: number=String with user's telephone number"""

        print "Authorizing..."
        path = '/insertalocalizador.do?telefono=' + number + '&submit.x=40&submit.y=5'
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie, 'Referer': 'http://www.localizame.movistar.es/buscalocalizadorespermisos.do'}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("GET", path, None, headers)
        resp=conn.getresponse()

        conn.close()

    def Unauthorize (self, number) :
        """Unauthorizes another user to locate us
            Input: number=String with user's telephone number"""

        print "Unauthorizing..."
        path = '/borralocalizador.do?telefono=' + number + '&submit.x=44&submit.y=8'
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie, 'Referer': 'http://www.localizame.movistar.es/login.do'}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("GET", path, None, headers)
        resp=conn.getresponse()

        conn.close()
        
    def Logout (self) :
        """Logs out from server"""
        
        print "Logout"
        headers = {"Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/vnd.ms-powerpoint, application/vnd.ms-excel, application/msword, application/x-shockwave-flash, */*", "Accept-Language": "es", "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)", "Connection": "Keep-Alive", "Cookie": self.cookie}
        conn=httplib.HTTPConnection("www.localizame.movistar.es")
        conn.request ("GET", "/logout.do",None, headers)
        resp=conn.getresponse()

        conn.close()

        self.Cookie = ''
