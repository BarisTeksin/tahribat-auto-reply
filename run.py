# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import time

headers = {'authority':'www.tahribat.com',
           'upgrade-insecure-requests':'1',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.72',
           'sec-fetch-user':'?1',
           'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'sec-fetch-site':'same-origin',
           'sec-fetch-mode':'navigate',
           'referer':'https://www.tahribat.com/',
           'accept-language':'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
           'cookie':'COOKIE_GELECEK_BURAYA'# COOKİE GELİYOR 
        }

ana_url = 'https://www.tahribat.com'
aranacak_kelimeler = ['TheAvenqer','TheAvenger','theavenqer','theavenger'] # MESAJLARDA ARANACAK KELİMELER ( NİCK )
yanit_yazildi = []
yanit = '<p>Deneme Mesajı</p>' # ALINTIYA YAZILACAK CEVABINIZ

r = requests.get('https://www.ou.edu/research/electron/internet/special.shtml')
soup = BeautifulSoup(r.content,'html.parser')
trler = soup.select('tr > td > font')
cevrilecek = {}
say = 0 
say2 = len(trler)-1
for x in trler:
    if say != 0 and say != say2:
        yazilar = x.text.split('\n')
        for yazi in yazilar:
            try:
                cevrilecek[yazi.split('\xa0 = \xa0')[0].strip()] = yazi.split('\xa0 = \xa0')[1].strip()
            except:
                pass
    say += 1

while True:
    r = requests.get(ana_url,headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    konu_urlleri = soup.select('table#activeTopics > tbody > tr > td > a')
    for konu_url in konu_urlleri:
        konu_linki = ana_url + konu_url.get('href') + '/'
        print(konu_linki)
        konu_id = konu_url.get('href').split('-')[-1]
        r = requests.get(konu_linki, headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        sayfa_sayisi = len(soup.select('.pagination > ul > li'))
        if sayfa_sayisi != 0:
            sayfa_sayisi = sayfa_sayisi - 2
        else:
            sayfa_sayisi = 2
        print(sayfa_sayisi)
        for sayfa in range(1,sayfa_sayisi):
            print(konu_linki + str(sayfa))
            r = requests.get(konu_linki + str(sayfa), headers=headers)
            soup = BeautifulSoup(r.content,'html.parser')
            messagelar = soup.findAll('li',attrs={'class':'ForumMessage'})
            for message in messagelar:
                message_tum = message.find('div',attrs={'class':'postMain'}).find('div',attrs={'class':'PostCanvas'}).find('div',attrs={'class':'PostContent'})
                alintilar = message.findAll('div',attrs={'class':'bunuyazdidiv'})
                message_text = str(message_tum)
                for alinti in alintilar:
                    message_text = message_text.replace(str(alinti),'')
                imza = str(message_tum.find('div',attrs={'class':'hide-for-small'}))
                duzenledi = str(message_tum.find('i',attrs={'style':'border-top: dotted 1px;font-size:0.9em'}))
                message_text = message_text.replace('<div class="PostContent">','').replace(imza,'')[:-6].replace(duzenledi,'').strip()
                for ara in aranacak_kelimeler:
                    if ara in message_text:
                        message_atilacak_url = message.find('div',attrs={'class':'postfoot'}).find('div',attrs={'class':'postFootRight hide-on-print'}).find('a',attrs={'class':'aquote'}).get('href')
                        try:
                            quote_id = str(message_atilacak_url).split('quote=')[1]
                            quote_folder = '0'
                        except:
                            quote_id = '0'
                            quote_folder = str(message_atilacak_url).split('quoteFolder=')[1]
                        if not str(message_atilacak_url) in yanit_yazildi:
                            r = requests.get(ana_url + message_atilacak_url, headers=headers)
                            soup = BeautifulSoup(r.content,'html.parser')
                            tokenimiz = soup.find('input',attrs={'name':'__RequestVerificationToken'}).get('value')
                            print(tokenimiz)
                            metin = str(soup.find('textarea',attrs={'id':'content'}).contents[0])
                            gonderilecek_genel = metin + yanit
                            for kelime,cevirisi in cevrilecek.items():
                                gonderilecek_genel = gonderilecek_genel.replace(kelime,cevirisi)
                            post = {'__RequestVerificationToken':tokenimiz,
                                    'quote':quote_id,
                                    'quoteFolder': quote_folder,
                                    'MessageId':'0',
                                    'FolderId':konu_id,
                                    'content':gonderilecek_genel,
                                    'submit':'Gönder'}
                            r2 = requests.post('https://www.tahribat.com/Forum/NewMessage',data = post,headers=headers)
                            print(r2)
                            yanit_yazildi.append(str(message_atilacak_url))
                            break
    time.sleep(1800)

