
from utils import *
from bs4 import BeautifulSoup
import re, requests, os
import pandas as pd

main_body_id = "_1TImB" #set the main body id
price_section_id = "_2sFaY" #set price section id
gallery_id = "_3cRjW" #set gallery section id
URL = "https://www.bearspace.co.uk/purchase?page=11" #listings
block_id = "_3Xnzg" #block id from a detailed listing page

products = available_listings(URL, block_id) #find the available products (except out of stock) and print 
print("Number of available products: {}".format(len(products))) 

listings = []

for product in products:
    soup = soup_content(product, main_body_id) #fetch content of webpage using BeauutifulSoup
    title = get_title(product, block_id, main_body_id) #get the title of the product
    price = get_price(product, block_id, price_section_id) #get the price of the product
    gallery_description = gallery_element(product, gallery_id, "p", "pre") #descrption of gallery block
    media, width, height = get_media_n_dimension(gallery_description) #get media, width and height
    print("URL: {}, Title: {}, Media: {}, Width: {}, Height: {}".format(product, title, media, width, height)) #print all fetched
    entries = {
        'url': product,
        'title':  title,
        'media': media,
        'height_cm': height,
        'width_cm': width,
        'price_gbp': price        
    }
    listings.append(entries)
print(listings)

df = pd.DataFrame.from_dict(listings) #creating pandas dataframe from the dictionary

df.to_csv("py_listings.csv") #save the dataframe in the form of .csv file
 