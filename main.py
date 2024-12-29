import pandas as pd
from bs4 import BeautifulSoup
import requests

# Función para guardar los datos de los productos
def export_csv(data):
    data = pd.DataFrame(data)
    data.to_csv("result.csv", index=False)

# Función para formatear el precio de un producto
def format_price(price):
    price = price.split(" ")[0]
    price = price.replace(".", "")
    price = price.replace(",", ".")
    return float(price)

def web_scrapping(url):
    res = {
        "Producto": [],
        "Precio": [],
    }
    req = requests.get(url)
    print(req.status_code)

    # Parsear el contenido de la página web
    soup = BeautifulSoup(req.content,"html.parser")

    # Extraer todos los contenedores de los productos
    productos = soup.find("div",attrs={"class":"product_list"}).find_all("article")

    # Iterar los productos dentro del arreglo de contenedores de productos
    for producto in productos:
        # Obtener nombre del producto
        name = producto.find("div", attrs={"class":"product-desc-wrap"}).find("div", attrs={"class":"name-product-list"}).find("a").text
        
        # Eliminar espacios en blanco al inicio y al final del nombre
        name = name.strip().rstrip()
        
        #Obtener el precio del producto
        price = producto.find("div", attrs={"class":"product-desc-wrap"}).find("div", attrs={"class":"product-price-and-shipping"}).find("span", attrs={"itemprop":"price"}).text
        price = format_price(price)
        res["Producto"].append(name)
        res["Precio"].append(price)

    return res

def main():
    url = "https://www.drogueriascafam.com.co/69-ofertas-destacadas-del-mes?resultsPerPage=48" # URL de la página web brindada utilizada en https://www.youtube.com/watch?v=9fGszA8DbOg 
    data = web_scrapping(url=url)
    export_csv(data)

if __name__ == "__main__":
    main()

