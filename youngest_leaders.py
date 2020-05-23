
## A program for finding the youngest heads of state and government by webscraping from wikipedia. 

from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
import lxml
from lxml import etree
import re
from datetime import datetime,date
import time


source = requests.get("https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government").text


tree = etree.HTML(source)

# Variables for storing the heads of state and governments
pm_dict = {}
president_dict = {}


print("Getting list of all heads of state and Government")

for i in range(2,213):
    
    # Skips switzerland and nauru (nauru's president doesnt have a birthdate in wikipedia)
    if i is 183 or i is 131:
        continue

    ## Country
    country = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/th/a/text()')
    if country == []:
        continue
    country = country[0]

    ## president
    president = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[1]/a[2]/text()')
    president_link = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[1]/a[2]/@href')

    # some countries entries dont have the same xpath for some reason, eg the interim president of bolivia
    if president == []:
        president = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td/span/a[2]/text()')[0]
        president_link = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td/span/a[2]/@href')[0]
    else :
        president = president[0]
        president_link = president_link[0]

    ## prime minister
    pm = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[2]/a[2]/text()')

    # If there's no prime minister, that must mean that its a president doing that job
    if pm == []:
        pm = f'(president) {president}'
        pm_link = president_link
    else:
        pm = pm[0]
        pm_link = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td[2]/a[2]/@href')[0]


    # other exceptions:
    
    # Brunei and Libya and oman 
    if i == 29 or i == 107 or i == 142:
        president = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td/a[3]/text()')[0]
        president_link = tree.xpath(f'//*[@id="mw-content-text"]/div/table[2]/tbody/tr[{i}]/td/a[3]/@href')[0]


    president_dict[country] = [president,president_link]
    pm_dict[country] = [pm,pm_link]



print("Gets Ages of presidents: ")

for country in president_dict:
    print("Getting the age of " + president_dict[country][0])

    try:
        source = requests.get(f"https://en.wikipedia.org{president_dict[country][1]}",timeout = 5).text
    except Timeout:
        print("Timeout")
        source = requests.get(f"https://en.wikipedia.org{president_dict[country][1]}",timeout = 5).text

    tree = etree.HTML(source)

    text = tree.xpath(f'//*[@id="mw-content-text"]/div/p/text()')

    ## Exceptions: (birthyear in different xpath)
    if country == 'Japan':
        text = tree.xpath('//*[@id="mw-content-text"]/div/p/span/text()')

    date = [i for i in text if bool(re.search(r'\d{4}',i))][0]
    end = re.search(r'\d{4}',date).end()
    try:
        start = re.search(r'\d{1} |\d{2} ',date).start()
    except:
        start = re.search(r'\d{4}',date).start()
    
    
    substring = date[start:end]



    if int(date[end-4:end]) > 2000:
        substring = "Failed to get age"

    president_dict[country].append(substring)

    #time.sleep(0.5)




## Pm ages
print("Gets the ages of prime ministers ")
for country in pm_dict:

    print("Getting the age of " + pm_dict[country][0]+ "'s head of state")

    if pm_dict[country][1][:5] != '/wiki':
        pm_dict[country].append("FalseLink")
        continue

    
    try:
        source = requests.get(f"https://en.wikipedia.org{pm_dict[country][1]}",timeout = 5).text
    except Timeout:
        print("Timeout")
        source = requests.get(f"https://en.wikipedia.org{pm_dict[country][1]}",timeout = 5).text




    tree = etree.HTML(source)

    text = tree.xpath(f'//*[@id="mw-content-text"]/div/p/text()')
    ## Exceptions: (birthyear in different xpath)
    if country == 'Japan':
        text = tree.xpath('//*[@id="mw-content-text"]/div/p/span/text()')


    date = [i for i in text if bool(re.search(r'\d{4}',i))][0]
    end = re.search(r'\d{4}',date).end()
    try:
        start = re.search(r'\d{1} |\d{2} ',date).start()
    except:
        start = re.search(r'\d{4}',date).start()
    
    
    substring = date[start:end]


    if int(date[end-4:end]) > 2000:
        substring = "Failed to get age"

    pm_dict[country].append(substring)
    #time.sleep(0.5)





print("Formatting data.. ")
## Making datetime objects in order to compare the birth years of leaders 
for country in president_dict:

    deit = president_dict[country][2]

    if deit[:2] == 'Fa' or len(deit)<4:
        president_dict[country].append("No Data")
        continue
    try:
        president_date = datetime.strptime(deit,'%d %B %Y')
    except ValueError:
        president_date = datetime.strptime(deit,'%Y')
    
    president_dict[country].append(president_date)

    deit = pm_dict[country][2]

    if deit[:2] == 'Fa' or len(deit)<4:
        pm_dict[country].append("No Data")
        continue
    try:
        pm_date = datetime.strptime(deit,'%d %B %Y')
    except:
        pm_date = datetime.strptime(deit,'%Y')
    
    pm_dict[country].append(pm_date)



# Final calculations and printing of results
youngest_pm_bday = max([pm_dict[i][3] for i in pm_dict if len(pm_dict[i]) > 3 and isinstance(pm_dict[i][3],datetime)])
youngest_pm_country = [i for i in pm_dict if pm_dict[i][3]==youngest_pm_bday][0]
youngest_pm_age = int((datetime.now().date() - youngest_pm_bday.date()).days//365.2422)

youngest_president_bday = max([president_dict[i][3] for i in president_dict if len(president_dict[i]) > 3 and isinstance(president_dict[i][3],datetime)])
youngest_president_country = [i for i in president_dict if president_dict[i][3]==youngest_president_bday][0]
youngest_president_age = int((datetime.now().date() - youngest_president_bday.date()).days//365.2422)


oldest_pm_bday = min([pm_dict[i][3] for i in pm_dict if len(pm_dict[i]) > 3 and isinstance(pm_dict[i][3],datetime)])
oldest_pm_country = [i for i in pm_dict if pm_dict[i][3]==oldest_pm_bday][0]
oldest_pm_age = int((datetime.now().date() - oldest_pm_bday.date()).days//365.2422)

oldest_president_bday = min([president_dict[i][3] for i in president_dict if len(president_dict[i]) > 3 and isinstance(president_dict[i][3],datetime)])
oldest_president_country = [i for i in president_dict if president_dict[i][3]==oldest_president_bday][0]
oldest_president_age = int((datetime.now().date() - oldest_president_bday.date()).days//365.2422)


print("Results:\nThe country with the youngest head of state is " + youngest_president_country+ ": " + president_dict[youngest_president_country][0] + " aged "+ str(youngest_president_age))
print("\nThe country with the youngest head of government is " + youngest_pm_country+ ": " + pm_dict[youngest_pm_country][0] + " aged "+ str(youngest_pm_age))

print("\nThe country with the oldest head of state is " + oldest_president_country+ ": " + president_dict[oldest_president_country][0] + " aged "+ str(oldest_president_age))
print("\nThe country with the oldest head of government is " + oldest_pm_country+ ": " + pm_dict[oldest_pm_country][0] + " aged "+ str(oldest_pm_age))

