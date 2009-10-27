# -*- coding: cp1252 -*-
# SMSSender API.
#
# Features:
# * Class Implementation to send an SMS message via web.

import httplib, urllib

class SMSSender:

    def SendMessage(self, login, pwd, dest, msg) :
        """Performs HTTP transactions against opensms server
            Input:  	login=String with user's telephone number
                      pwd=String with user's password
                      dest=String with destination telephone number
                      msg=String with message text"""

        params1 = urllib.urlencode ({'TM_ACTION': 'AUTHENTICATE', 'TM_LOGIN': login})
        params2 = urllib.urlencode ({'TM_PASSWORD': pwd})
        params3 = urllib.urlencode ({'to': dest, 'message': msg})
        params = params1 + "&" + params2 + "&" + params3
        headers = {"Content-type":"application/x-www-form-urlencoded","Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive"}
        conn=httplib.HTTPSConnection("opensms.movistar.es")
        conn.request ("POST", "/aplicacionpost/loginEnvio.jsp",params, headers)
        resp=conn.getresponse()
        response=resp.read()

        conn.close()
        
        return response
