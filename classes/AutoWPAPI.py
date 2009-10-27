# -*- coding: cp1252 -*-
# AutoWP API.
#
# Features:
# * Class Implementation to send an SMS message via web.

import httplib, urllib

class AutoWP:

    def SendAutoWP(self, login, pwd, url, text) :
        """Performs HTTP transaction to send autoWP
            Entrada:  login=String with user's telephone number
                      pwd=String with user's password
                      url=String with message URL
                      text=String with message text"""

        params = urllib.urlencode ({'TME_USER': login, 'TME_PASS': pwd, 'WAP_Push_URL': url, 'WAP_Push_Text': text})
        headers = {"Content-type":"application/x-www-form-urlencoded","Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*", "User-Agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)", "Connection" :  "Keep-Alive"}
        conn=httplib.HTTPConnection("open.movilforum.com")
        conn.request ("POST", "/apis/autowap",params, headers)
        resp=conn.getresponse()
        response=resp.read()

        print response

        conn.close()
        
        return response
