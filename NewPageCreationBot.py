# -*- coding: utf-8 -*-

import urllib2
import requests

user='Wikipastbot'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='Créatibot update'

names=['Madame X','Monsieur Y']

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

for name in names:
    content=''
    content+='==Biographie==\n'
    content+='Veuillez écrire une biographie ici\n'
    content+='==Références==\n'
    content+='=== Ngrams viewer ===\n'
    name_ngv=name.lower().replace(" ","%20")
    content+='[http://dhlabsrv4.epfl.ch/ngviewer.php?mode=1&req_1='+name_ngv+' '+name+']\n'
    content+='=== Archives Le Temps ===\n'
    # save action
    headers={'content-type':'application/x-www-form-urlencoded'}
    payload={'action':'edit','assert':'user','format':'json','text':content,'summary':summary,'title':name,'token':edit_token}
    r4=requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
    print(r4.text)
