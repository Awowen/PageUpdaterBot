# @Author: Uran Axel <mineuran>
# @Date:   2016-03-24T14:18:19+01:00
# @Email:  axel.ursc@gmail.com
# @Last modified by:   Awowen
# @Last modified time: 2016-04-05T14:47:13+02:00


# -*- coding: utf-8 -*-

"""
Bot qui surveille toutes les nouvelles entrées biographiques et met à jour les pages concernant les entités présentes automatiquement. Si la page n'existe pas il la créé.  Exemple : Un utilisateur qui met à jour la page Henri Dunant rentre l'information  1864.08.22 / Genève. Création par Henri Dunant de la Croix rouge. [5] Le bot recopie la ligne à la bonne place sur la page Croix rouge.
"""

import urllib2
import requests
from bs4 import BeautifulSoup

############# Création des parametre ##########################

user='PageUpdaterBot'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='PageUpdaterBot'

############## Login request ##################################

r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

############## login confirm ##################################

login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)

baseurl = 'http://wikipast.world/wiki/'
names = []
with open('listofpages.txt') as f:
    names = names + [f.readlines()]

for name in names:
    result=requests.post(baseurl+'api.php?action=query&titles='+name+'&export&exportnowrap')
    soup=BeautifulSoup(result.text)
    code=''
    for primitive in soup.findAll("text"):
        code+=primitive.string
    print(code)

# TODO
"""
Click on every link
If link already exist --> if the change has not been made --> change the page
If redlink --> Create new page
"""
