# Web Scrapping Task

I was looking for a challenge for a web crawling and somewhere, I found a task to crawl a webpage: https://www.bearspace.co.uk/purchase

We will crawl a gallery's listing of works available for sale.
The listings are on https://www.bearspace.co.uk/purchase

Each listing leads to a detail page. 
*E.g.* https://www.bearspace.co.uk/product-page/combe-martin-1-emerald-by-phil-ashcroft.

**Task**: Scrape all artworks available for sale.

**Output**: The main function should generate a CSV that gets saved to the current working
directory. The CSV should have the following format :


| url | title | media | height_cm | width_cm | price_gbp | 
| ------ | ------ | ------ | ------ | ------ | ------ |
| www.product_page.com | canvas | The artistic  | 25 | 25 | 350 |


### Dependancies 
 Python 3
 ```
 BeautifulSoup 4.8.0
 requests 2.22.0 
 pandas 0.25.1
 ```