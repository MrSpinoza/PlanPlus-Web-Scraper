"" Created on Sat Jan 29 18:41:30 2022

@author: MACEDOLJANB """

from bs4 import BeautifulSoup import requests import pandas as pd

# Gradovi u pretrazi
grad = ['beograd', "novi-sad", 'nis', 'kragujevac', 'subotica', 'leskovac', 'zrenjanin', 'pancevo', 'cacak', 'novi-pazar', 'kraljevo', 'smederevo', 'valjevo', 'krusevac', 'vrsac', 'vranje', 'sabac', 'uzice', 'sombor', 'pozarevac', 'zajecar', 'sremsa-mitrovica', 'jagodina', 'loznica', 'pristina', 'kosovska-mitrovica', 'podgorica', 'niksic', 'bar']

# Prazne liste za kolone u df
zemlja_list = [] grad_list = [] postanski_broj_list = [] adresa_list = [] sajt_list = [] ftelefon_list = [] mtelefon_list = [] mejl_list = []

for grad in grad: # Pocetna stranice kategorije: url_poc = 'https://www.planplus.rs/adresar/{}/arhitektura-i-projektovanje/'.format(grad)

# Funkcija za skidanje podataka:
def skidac(url):
    web_content = requests.get(url).text
    soup = BeautifulSoup(web_content, "lxml")
    data_1= soup.find('div', attrs={'class': 'group info'})
    data_2 = soup.find_all('div', attrs={'class': 'web'})
    print(data_2)
    data_3 = soup.find_all('div', attrs = {'class': 'telephone'})
    postanski_broj = data_1.span.text
    adresa = data_1.div.div.text
    grad = data_1.div.find_all('span')[1].text
    if not data_3:
        ftelefon = None
        mtelefon = None
    else:
        if len(data_3) == 2:
            ftelefon = data_3[0].span.text
            mtelefon = data_3[1].span.text
        else:
            ftelefon = data_3[0].span.text
            mtelefon = None
    zemlja = data_1.meta['content']
    if not data_2:
        mejl = None
        sajt = None
    else:
        if len(data_2)==2:
            sajt = data_2[0].a['href'].split(":")[1]
            mejl = data_2[1].a['href'].split(":")[1]
        elif len(data_2)==1:
            if data_2[0].a['href'].startswith("http"):
                sajt = data_2[0].a['href'].split(":")[1]
                mejl= None
            else:
                sajt = None
                mejl = data_2[0].a['href'].split(":")[1]
    return [zemlja, grad, adresa, postanski_broj, ftelefon, mtelefon, sajt, mejl]


for i in range(1,500):
    url = url_poc+str(i)
    web_content = requests.get(url).text
    soup = BeautifulSoup(web_content, "lxml")
    greska_1 = soup.find("div", attrs={'class':'error tcenter'}) #Ukoliko ima class:error tcenter onda nema vise te stranice
    data = soup.find_all('div', attrs={'class': 'geodir-category-header'})
    print(data)
    for data in data:
        url = 'https://www.planplus.rs'+data.a['href']
        print(url)
        zemlja_list.append(skidac(url)[0])
        grad_list.append(skidac(url)[1])
        adresa_list.append(skidac(url)[2])
        postanski_broj_list.append(skidac(url)[3])
        ftelefon_list.append(skidac(url)[4])
        mtelefon_list.append(skidac(url)[5])
        sajt_list.append(skidac(url)[6])
        mejl_list.append(skidac(url)[7])
    if greska_1 != None:
        break
# Pravljenje df-a od lista
df=pd.DataFrame({ 'Drzava': zemlja_list, 'Grad': grad_list, 'Posta': postanski_broj_list, 'Adresa': adresa_list, 'Mobilni Telefon': mtelefon_list, 'Fiknsi Telefon': ftelefon_list, 'e-mail': mejl_list, 'Web Sajt': sajt_list })

# Cuvanje podataka u csv format
dt_name="PlanPlus_izvod" df.to_csv(dt_name+".csv",encoding='utf-8-sig')

# Zavrsna poruka
print("Sacuvano, zavrseno!")

© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
