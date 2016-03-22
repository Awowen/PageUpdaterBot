# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

baseurl='http://wikipast.world/wiki/'

names=['Henri_Dunant']

for name in names:
    result=requests.post(baseurl+'api.php?action=query&titles='+name+'&export&exportnowrap')
    soup=BeautifulSoup(result.text)
    code=''
    for primitive in soup.findAll("text"):
        code+=primitive.string
    print(code)
