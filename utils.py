from bs4 import BeautifulSoup
import re, requests, json
import pandas as pd

def available_listings(URL, block_id):
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find_all(class_="_2zTHN")
    
    links = []
    for i in results:
        link_elems = i.find_all('a')
        link = [l.get('href') for l in link_elems] #find all the hrefs within the block
        price_elems = i.find_all('span', class_='_23ArP') #get the price element by its class_id
        #filter out "out of stock" 
        try:
            test = price_elems[0]
        except IndexError:
            pass
        else:
            links.extend(link)
    return links

def soup_content(url , block_id):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def get_title(url, block_id, main_body_id):
    soup = soup_content(url, block_id)
    main_body = soup.find(class_ = main_body_id)
    title = [t.text for t in main_body.find_all('h1')]
    return  title[0]

def get_price(url, block_id, price_section_id):
    soup = soup_content(url, block_id)
    price_section = soup.find(class_= price_section_id)    
    price = [p.text for p in price_section.find_all("span")]    
    price =  price[0]
    return re.sub('[£$,]', '', price) #remove currency symbol    

def gallery_element(url, gallery_id, tag):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")        

    gallery = soup.find(class_=gallery_id)
    gallery_root = gallery.find_all(tag)
    gallery_description = [i.text for i in gallery_root][:3]
    gallery_description.sort()
    if 'x' not in str(gallery_description[0]).lower():
        del gallery_description[0]
    elif '2019' in gallery_description[1]:
        del gallery_description[1]
    elif '2020' in gallery_description[1]:
        del gallery_description[1]
    else:
        pass
    return gallery_description

def get_media_n_dimension(gallery_descrption):
    if len(gallery_descrption) == 2:
        dim = gallery_descrption[0]
        media = gallery_descrption[1]
    else:
        dim = gallery_descrption[0]
        media = ' '.join(gallery_descrption[1:2])
    str_todigit= re.findall(r'\d+(?:\.\d+)?', dim)

    try:
        width  = str_todigit[0] 
        height = str_todigit[1]    
    except IndexError:
        width = 00
        height = 00
    return media, width, height



