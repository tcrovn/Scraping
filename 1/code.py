#Connecting new libraries
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Accept": "image/avif,image/webp,*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

#Function for downloading pictures from the site
def download(url):
    resp = requests.get(url, stream=True)
    r = open("\\home\\danko\\Documents\\python\\scraping\\projects\\first_project\\" + url.split("/")[-1], "wb")
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()

#Function to take the link of each product from the page
def get_url():
    for count in range(1, 8):

        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

        for i in data:
            product_url = "https://scrapingclub.com" + i.find("a").get("href")
            yield product_url

product_info = []
#A cycle that goes through each product link and takes product information
for card_url in get_url():

    response = requests.get(card_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find("div", class_="card mt-4 my-4")
    name = data.find("h3", class_="card-title").text
    price = data.find("h4").text
    product_details = data.find("p", class_="card-text").text
    img_url = "https://scrapingclub.com" + data.find("img", class_="card-img-top img-fluid").get("src")
    download(img_url)
    product_info.append(
        {
            "Name:": name,
            "Price": price,
            "Product description": product_details,
            "Image url": img_url
        }
    )
     #Write the required data about the product to the json file
    with open(f"product_info.json", "w") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
