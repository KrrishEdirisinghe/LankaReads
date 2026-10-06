from bs4 import BeautifulSoup
import requests




def scrape_md(query):
    query= query.replace(" ","+")
    url = f"https://mdgunasena.com/?s={query}&post_type=product&dgwt_wcas=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    products = soup.find_all("div", class_="product")
    books = []
    for product in products:
        
        title = product.find("h3", class_="product-title")
        price = product.find("span", class_="price")
        img = product.find("img", class_="attachment-woocommerce_thumbnail")

        if title and price and img:

            price = price.find("bdi").get_text()
            price = price.replace("රු", "")
            price = price.replace(",", "")
            
            books.append({
                "store": "MDgunasekera",
                "title": title.get_text(strip=True),
                "price": float(price),
                "img": img["src"]
            })
    return books

  