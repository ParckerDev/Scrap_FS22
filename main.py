import requests
from bs4 import BeautifulSoup as Bs
import pandas as pd
from time import sleep

def pagination(url):
    htmls = requests.get(url).text
    try:
        page = int(Bs(htmls, 'html.parser').find('ul', class_='pagination text-center clearfix').findAll('a')[-1].text) # type: ignore
    except:
        page = 1
    return page

def link_slice(link):
    new_link = link.split('page=0')
    return new_link


def make_category(url):
    html = requests.get(url).text
    soup = Bs(html, 'html.parser').find('ul', class_='tabs-mods-category-list').findAll('a') # type: ignore
    categories = [[category.text, 'https://www.farming-simulator.com/'+category.get('href')] for category in soup]
    return categories

url = 'https://www.farming-simulator.com/mods.php'
categories = make_category(url)
new_data = []
for category in categories[:1]: #количество категорий
    for i in range(pagination(category[1])):

        page = f'{link_slice(category[1])[0]}page={i}'
        html = requests.get(page).text
        print(page) # after work delete
        cards = Bs(html, 'html.parser').findAll('div', class_='medium-6 large-3 columns')
        for card in cards:
            cat = category[0]
            name = card.find('h4').text
            try:
                rate = float(card.find('div', class_="mod-item__rating-num").text.rstrip().split()[0])
                downloads = int(card.find('div', class_="mod-item__rating-num").text.rstrip().split()[1][1:-2])
            except:
                rate = 0
                downloads = 0
            link = 'https://www.farming-simulator.com/'+card.find('a', class_='button button-buy button-middle button-no-margin expanded').get('href')
            new_data.append([cat, name, rate, downloads, link])
            #print(f'Category - {cat}\nname - {name}\nrate - {rate}\ndownloads - {downloads}\nlink - {link}\n')
        sleep(2)
print(new_data)
header = ['Category', 'Name', 'Rate', 'Downloads', 'Link']
mods = pd.DataFrame(new_data, columns=header)
mods.to_csv('farming_mods.csv', sep=';', encoding='utf8')
