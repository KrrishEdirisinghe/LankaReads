from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
import json

def scrape_sarasavi(query):
    
    
    search_url = f"https://sarasavi.lk/serach-result?keyword={quote_plus(query)}"
    
    response = requests.get(search_url)
    
    soup = BeautifulSoup(response.text,"html.parser")
    
    data = soup.find("script",id="__NEXT_DATA__").text
    
    json_data = json.loads(data)

    
    products = json_data["props"]["pageProps"]["initialResults"]["data"]
    for product in products:
        product["image"] = "https://cms.sarasavi.lk/storage/" + str(product["image"])
    books = []

    for book in products:
        books.append({"store":"sarasavi","title":book["name"], "price":float(book["promotion"]["discounted_price"]),"img":book["image"]})
    return books
