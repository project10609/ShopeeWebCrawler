# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup



class Shopeebrow1Spider(scrapy.Spider):
    name = 'shopeebrow1'

    start_urls = ['https://shopee.tw/search?category=67&facet=15726&keyword=%E7%9C%89%E5%BD%A9%E9%A1%9E%E7%94%A2%E5%93%81&page=0&subcategory=15701']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/search?category=67&facet=15726&keyword=%E7%9C%89%E5%BD%A9%E9%A1%9E%E7%94%A2%E5%93%81&page=0&subcategory=15701&page=' + str(
            Shopeebrow1Spider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text.replace(',','')
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'Brow'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            i['product_subcategory'] = 'brow'

            yield i

        if Shopeebrow1Spider.page <= 20:
            Shopeebrow1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
