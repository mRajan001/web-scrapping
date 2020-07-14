from bs4 import BeautifulSoup
import re, requests, json
import pandas as pd

def available_listings(URL, block_id):
    """
    A function to find all the available listing from a given homepage. 
    Input: Takes in a URL which needs to be scrapped.
    Output: Available listing except out of stock
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_="_2zTHN") 
    
    links = []
    for i in results:
        link_elems = i.find_all('a') 
        link = [l.get('href') for l in link_elems] #find all the hrefs within the block
        price_elems = i.find_all('span', class_='_23ArP') #get the price element by its class_id 
        #filter out "out of stock" 
        try:
            price_elems[0] #check if price_elems is empty
        except IndexError:
            pass
        else:
            links.extend(link)
    return links

def soup_content(url , block_id):
    """
    A simple function returns BeautifulSoup object
    """
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def get_title(url, block_id, main_body_id):
    """
    A function to get the title of the listing. 
    Input: 
        url (this will be one of the list entry from "available listings")
        block_id: A block id of
    Output: 
    """
    soup = soup_content(url, block_id)
    main_body = soup.find(class_ = main_body_id)
    title = [t.text for t in main_body.find_all('h1')]
    return  title[0] #title is the 1st element of the list

def get_price(url, block_id, price_section_id):
    """
    A function to get the price.
    Input: 
        url= listing page url
        block_id= block id of listing detail page
        price_section_id= price section id
    Output:
        Integer price without currency symbol
    """
    soup = soup_content(url, block_id)
    price_section = soup.find(class_= price_section_id)    
    price = [p.text for p in price_section.find_all("span")]    #Product "price" is inside "span"
    price =  price[0]
    return re.sub('[£$,]', '', price) #remove currency symbol    

def gallery_element(url, gallery_id, tag, alt_tag):
    """
    The listing page contains details such as media, width and height of the product in gallery section.
    This function helps us to get to those information.
    
    Input:
        url= listing url
        gallery_id = gallery section ID.
        tag= HTML tag containing information such as media, width and height
        alt_tag= HTML tag containing information. If above "tag" returns an empty list, this tag will be checked.
    Output:
        Gallery discription as a list
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")        

    gallery = soup.find(class_=gallery_id) 
    gallery_root = gallery.find_all(tag) #finding all "p" tags
    gallery_description = [i.text for i in gallery_root][:3] #all the required infomation are within this range
    gallery_description.sort() #sort the list, to get product dimension at the first place in the list

    if len(gallery_description) == 0: #if tag "p" is not present, gallery_description could be just within tag "pre"
        gallery_root = gallery.find_all(alt_tag) #get the information from "pre" tag.
        gallery_description = [i.text for i in gallery_root][:3] #all the required infomation are within this range
        gallery_description.sort()
    
    #media, width and height are randomly placed within the gallery section for some listings.

    elif 'x' not in str(gallery_description[0]).lower(): 
        del gallery_description[0]
    elif '2019' in gallery_description[1]:
        del gallery_description[1]
    elif '2020' in gallery_description[1]:
        del gallery_description[1]
    else:
        pass
    return gallery_description

def get_media_n_dimension(gallery_descrption):
    """
    A function to get information retrieved from "gallery_element"
    Input: A gallery description. An output of gallery element.
    Output:
        media, width and height of liting
    """

    if len(gallery_descrption) == 2:
        dim = gallery_descrption[0]
        media = gallery_descrption[1]
    else:
        dim = gallery_descrption[0]
        media = ' '.join(gallery_descrption[1:2]) #join media if in multiple lines
    str_todigit= re.findall(r'\d+(?:\.\d+)?', dim) 

    try:
        width  = str_todigit[0] 
        height = str_todigit[1]    
    except IndexError:
        width = 00
        height = 00
    return media, width, height



