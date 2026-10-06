from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
import json


def scrape_jeya(query):
    search_url = f"https://jeyabookcentre.com/search?key={quote_plus(query)}"
  
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text,"html.parser")
    
    data = soup.find("script", id="__NEXT_DATA__").text
    
    json_data = json.loads(data)
   

    products = json_data["props"]["pageProps"]["products"]
    books = []
    for book in products:
        books.append({"store":"jeya book center","title":book["item_title"], "price":float(book["unit_price"]),"img":book["cover_img"]})
    return books

