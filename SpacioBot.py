# -*- coding: utf-8 -*-

import urllib2
import requests
import math

user='Wikipastbot'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='Spaciobot update'

nom_lieux=['Genève','Lausanne']
# Attention : La longitude est donnée en premier pour avoir une référentiel directe en coordonnées ellipsoïdales.
pos_lieux=[[[6,8,44],[46,12,8],0],[[6,37,58],[46,20,57],0]]

def degre_to_radiant(data):
    degre=1.0*data[0]+1.0*data[1]/60.0 + 1.0*data[2]/3600.0
    radiant=degre*math.pi/180.0
    return radiant

pos_lieux_rad=[]
for i in range(len(pos_lieux)):
    temp=[]
    temp.append(degre_to_radiant(pos_lieux[i][0]))
    temp.append(degre_to_radiant(pos_lieux[i][1]))
    temp.append(pos_lieux[i][2])
    pos_lieux_rad.append(temp)

pos_lieux_convert=[]

LE_GEODESY_LMIN=-1.0*math.pi
LE_GEODESY_LMAX=1.0*math.pi
LE_GEODESY_AMIN=-1.0*math.pi/2.0
LE_GEODESY_AMAX=1.0*math.pi/2.0
LE_GEODESY_HMIN=-2*math.pi*6378137.0/1024.0
LE_GEODESY_HMAX=2*math.pi*6378137.0/1024.0

for i in range(len(nom_lieux)):
    le_pose=pos_lieux_rad[i]
    longeur_adress=20
    le_address=longeur_adress*[0]

    le_buffer=0
    le_parse=0

    le_pose[0]=(le_pose[0]-LE_GEODESY_LMIN)/(LE_GEODESY_LMAX-LE_GEODESY_LMIN)
    le_pose[1]=(le_pose[1]-LE_GEODESY_AMIN)/(LE_GEODESY_AMAX-LE_GEODESY_AMIN)
    le_pose[2]=(le_pose[2]-LE_GEODESY_HMIN)/(LE_GEODESY_HMAX-LE_GEODESY_HMIN)

    for le_parse in range(longeur_adress):
        if le_pose[0] >= 0.5:
            le_buffer = 1
        else:
            le_buffer = 0
        le_address[le_parse]=le_buffer
        le_pose[0] = ( le_pose[0] * 2.0 ) - le_buffer

        if le_parse >= 1:
            if le_pose[1] >= 0.5:
                le_buffer = 1
            else:
                le_buffer = 0
            le_address[le_parse]=le_address[le_parse]+le_buffer*2
            le_pose[1]=(le_pose[1]*2.0)-le_buffer

            if(le_parse>=10):
                if le_pose[2]>=0.5:
                    le_buffer=1
                else:
                    le_buffer=0
                le_address[le_parse]=le_address[le_parse]+le_buffer*4
                le_pose[2]=(le_pose[2]*2.0)-le_buffer
    for j in range(len(le_address)):
        le_address[j]=str(le_address[j])
    pos_lieux_convert.append(''.join(le_address))
    print(str(nom_lieux[i])+' => '+''.join(le_address))

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

for i in range(len(nom_lieux)):
    content='\n==Lieu: '+str(nom_lieux[i])+'=='
    # save action
    headers={'content-type':'application/x-www-form-urlencoded'}
    #payload={'action':'edit','assert':'user','format':'json','text':content,'summary':summary,'title':pos_lieux_convert[i],'token':edit_token}
    payload={'action':'edit','assert':'user','format':'json','appendtext':content,'summary':summary,'title':pos_lieux_convert[i],'token':edit_token}
    r4=requests.post(baseurl+'api.php',headers=headers,data=payload,cookies=edit_cookie)
    print(r4.text)
