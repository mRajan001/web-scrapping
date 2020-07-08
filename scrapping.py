from utils import *
from bs4 import BeautifulSoup
import re, requests, os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# blocks IDs fetched by inspecting the element of the webpage
main_body_id = "_1TImB" # from URL = "https://www.bearspace.co.uk/purchase"
price_section_id = "_2sFaY" #from individual product page
gallery_id = "_28cEs"

products = get_href(URL, block_id)
print("{} products found in total.".format(len(products)))

