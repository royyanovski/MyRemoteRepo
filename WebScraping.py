import sys

import requests  # A package for downloading HTML code from a website.

from bs4 import BeautifulSoup  # A package for parsing HTML code.

url_address_pattern = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&LH_TitleDesc=0&_pgn=1'  # The page i'm working on.

NO_OF_PAGES_TO_EXAMINE = 4 # add 2 to the page no. you want it to get to.
SMARTPHONE_MODELS = ['iphone', 'samsung+galaxy', 'xiaomi+mi', 'huawei+p']


def get_data(link_list):  # Extracting the data we are interested in.
    for link in link_list:
        item_page = requests.get(link)
        item_soup = BeautifulSoup(item_page.content, 'html.parser')
        item_results = item_soup.find(id="Body")
        title_elem = item_results.find('h1', class_='it-ttl')
        try:
            price_elem = item_results.find('div', class_='u-flL w29 vi-price').find('span', class_='notranslate')
        except:
            price_elem = item_results.find('span', class_='notranslate')
        location_elem = item_results.find('div', class_='iti-eu-bld-gry')
        shipment_elem = item_results.find('span', class_='notranslate sh-cst')
        condition_elem = item_results.find('div', class_='u-flL condText')

        if title_elem == None:
            pass
        else:
            title_elem.find('span', class_='g-hdn').decompose()
        if shipment_elem == None:
            pass
        else:
            shipment_elem.find('span', class_='sh-svc sh-nwr').decompose()

        chosen_elements = [title_elem, price_elem, location_elem, shipment_elem, condition_elem]

        for elem in chosen_elements:
            if elem != None:
                print(elem.text.strip())
        print()


def roy_and_roi_webscraper(url):
    """Webscraping function for ebay. Running on a pre-determined number of search pages,
    starting from the entered first search page. Output: prints title, price, supplier country,
    and shipping cost for each item."""
    for page_no in range(2, NO_OF_PAGES_TO_EXAMINE):
        links = []
        try:
            page = requests.get(url)  # Getting the HTML code.
        except Exception:
            sys.exit()
        else:
            soup = BeautifulSoup(page.content, 'html.parser')  # Creating BS object to work on with an HTML parser.
            results = soup.find(id="mainContent")  # Extracting the results of the ebay search.
            product_items = results.find_all('li', class_='s-item')  # Separating and using only the results themselves.
            for product_item in product_items:  # Getting the links for the product pages.
                try:
                    link = product_item.find('a')['href']
                except Exception:
                    continue
                else:
                    links.append(link)
            get_data(links)
            url = url[:-1] + str(page_no)


def main(url_pattern):
    for model in SMARTPHONE_MODELS:
        url_address = url_pattern.format(model)
        roy_and_roi_webscraper(url_address)


if __name__ == "__main__":
    main(url_address_pattern)



### Other Options:


## Searching only for 'iPhone X' products (as an example):

#def look_for_iphonex(text):
#    """If the entered text is not None, the function returns strings that
#    contain 'iphone x'"""
#    if text != None:
#        return 'iphone x' in text.lower()

# iphonex_products = results.find_all('h3', string=lambda text: look_for_iphonex(text))

## Retrieving the links for the product pages of products:

#for product_item in product_items:
#    try:
#        link = product_item.find('a')['href']
#    except Exception:
#        continue
#    else:
#        print(product_item.text.strip())
#        print(f'Link to product page: {link}\n')