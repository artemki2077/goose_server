import multiprocessing

from schemas.product import Product
import requests
from bs4 import BeautifulSoup as bs4
import datetime as dt


class WishMaster:

    def get(self) -> list[Product]:
        links = ['https://wishmaster.me/catalog/smartfony/', 'https://wishmaster.me/catalog/televizory_monitory/monitory/']
        data = []
        for link in links:
            data += self.get_all_from(link, count_process=20)
        return data

    def get_html(self, url):
        respons = requests.get(url)
        return bs4(respons.text, 'html5lib')

    def get_pages(self, args):
        n, link = args
        pages = self.get_html(f'{link}?PAGEN_2={n}')
        element = pages.find_all('div', {'class': 'product-item'})
        products = []
        for index_elem, i in enumerate(element):
            try:
                elem_time_image_wrap = i.find("a", {"class": "product-item-image-wrapper"})
                original_link = "https://wishmaster.me" + elem_time_image_wrap['href']
                name = elem_time_image_wrap['title']
                price_elem: str = i.find('span', {'class': "product-item-price-current"}).text
                price = int(price_elem.strip()[:-5].replace(" ", ""))
                dts = list(map(lambda x: x.text.strip(), i.find_all("dt")))
                dds = list(map(lambda x: x.text.strip() if x.find("a") is None else x.find("a").text.strip(), i.find_all("dd")))
                add_data = dict(zip(dts, dds))
                img_url = None
                elem_img_link = i.find("span", {'class': 'product-item-image-original'})
                if elem_img_link is not None:
                    img_url = "https://wishmaster.me" + elem_img_link['style'][23:-4]
                products.append(Product(
                    last_update=dt.datetime.now(),
                    name=name,
                    price=float(price),
                    original_link=original_link,
                    add_data=add_data,
                    img_url=img_url
                ))
            except Exception as e:
                print(e)
                print(n, link)
                print(index_elem)
        return products

    def get_all_from(self, link='https://wishmaster.me/catalog/smartfony/', count_process=5):
        product = []
        product_pages = self.get_html(f'{link}')
        count_pages = int(product_pages.find('div', {"class": "nums"}).find_all('a')[-1].text)
        with multiprocessing.Pool(count_process) as p:
            for i in p.map(self.get_pages, list(map(lambda x: [x + 1, link], range(0, count_pages)))):
                product += i
        return product