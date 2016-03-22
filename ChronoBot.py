# -*- coding: utf-8 -*-

import urllib2
import requests
import datetime

user='Wikipastbot'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='Chronobot update'

dates=['0033/06/02']
dates_convert=[]

for date in dates:
    the_date=datetime.datetime.strptime(date, "%Y/%m/%d")
    timestamp=(the_date-datetime.datetime(1970, 1, 1)).total_seconds()+36
    convert=int(1.0*timestamp/(24*3600))
    dates_convert.append(str(convert))
    print(str(date)+' => '+str(convert))

# Login request
r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

#login confirm
login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)

#get edit token2
params3='?format=json&action=query&meta=tokens&continue='
r3=requests.get(baseurl+'api.php'+params3,cookies=r2.cookies)
edit_token=r3.json()['query']['tokens']['csrftoken']

edit_cookie=r2.cookies.copy()
edit_cookie.update(r3.cookies)

for i in range(len(dates)):
    content='\n==Date: '+str(dates[i])+'=='
    # save action
    headers={'content-type':'application/x-www-form-urlencoded'}
    #payload={'action':'edit','assert':'user','format':'json','text':content,'summary':summary,'title':dates_convert[i],'token':edit_token}
    payload={'action':'edit','assert':'user','format':'json','appendtext':content,'summary':summary,'title':dates_convert[i],'token':edit_token}
    r4=requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
    print(r4.text)
