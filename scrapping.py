
from utils import *
from bs4 import BeautifulSoup
import re, requests, os
import pandas as pd

main_body_id = "_1TImB"
price_section_id = "_2sFaY"
gallery_id = "_3cRjW"#"_28cEs"
URL = "https://www.bearspace.co.uk/purchase?page=10"
block_id = "_3Xnzg"

products = available_listings(URL, block_id) #find the available products (except out of stock)
print("Number of available products: {}".format(len(products)))

listings = []

for product in products:
    soup = soup_content(product, main_body_id)
    title = get_title(product, block_id, main_body_id)
    price = get_price(product, block_id, price_section_id)
    # print(price)
    # gallery_soup = soup_content(product, gallery_id)
    # gallery_root = gallery_soup.find("p")
    gallery_description = gallery_element(product, gallery_id, "p") #upto here this is dn
    # print(gallery_description)
    media, width, height = get_media_n_dimension(gallery_description)
    print("URL: {}, Title: {}, Media: {}, Width: {}, Height: {}".format(product, title, media, width, height))
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

df = pd.DataFrame.from_dict(listings)

df.to_csv("py_listings.csv")


