# @Author: Uran Axel <mineuran>
# @Date:   2016-03-24T14:18:19+01:00
# @Email:  axel.ursc@gmail.com
# @Last modified by:   Awowen
# @Last modified time: 2016-04-05T13:17:39+02:00


# -*- coding: utf-8 -*-

import urllib2
import requests

user='PageUpdaterBot'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='PageUpdaterBot'

# Login request
r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

#login confirm
login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)
