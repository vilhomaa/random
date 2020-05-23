
from bs4 import BeautifulSoup
import requests
import lxml
from lxml import etree
import re

# In finnish sry, say if translations or further explanations are needed
### Ohjelman idea: löytää nuorimpana aloittanut suomen pääministeri

## OHJELMAN KUVAUS: Hakee Wikipediasta kaikkien suomen pääministereiden syntymäajat ja pääministerinä aloittamisen vuoden.
# Sitten ohjelma ottaa erotuksen näistä ja etsii nuorimpana aloittaneen pääministerin.


source = requests.get("https://fi.wikipedia.org/wiki/Luettelo_Suomen_p%C3%A4%C3%A4ministereist%C3%A4").text



tree = etree.HTML(source)

pm_dict = {}

# Hakee pressojen nimet ja niiden indeksin html:s ja sen xpathis
# Huom alottaa indeksien looppaamisen lopusta. jos joku on ollut 2 krt pm, niin sen ensimmäisen tiedot tallentuu dictiin
for i in reversed(range(3,145)):

    pm_nimi = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[3]/b/a/text()')

    if len(pm_nimi) == 1:
        pm_dict[pm_nimi[0]] = [i]


# Hakee indeksin avulla niiden elinvuodet ja aloitusvuoden
for i in pm_dict:

    svuosi = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{pm_dict[i][0]}]/td[3]/small/text()')[0]
    svuosi = int(re.findall('\d+', svuosi)[0])
    pm_dict[i].append(svuosi)

    alovuosi = tree_text = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{pm_dict[i][0]}]/td[4]/text()')[0]
    alovuosi = int(re.sub('\D','', alovuosi))
    pm_dict[i].append(alovuosi)

    pm_dict[i] = pm_dict[i][1:]



# Ottaa syntymäiän ja alotusvuoden erotuksen
for i in pm_dict:

    alotusika = pm_dict[i][1]-pm_dict[i][0]
    pm_dict[i].append(alotusika)

    pm_dict[i] = pm_dict[i][2:]


nuorin = min(pm_dict,key=pm_dict.get)

print(f'Nuorin Suomen pääministeri kautta aikojen on: {nuorin}')



