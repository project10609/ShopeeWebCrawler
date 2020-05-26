# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup

class Shopeeremover1Spider(scrapy.Spider):
    name = 'shopeeremover1'

    start_urls = ['https://shopee.tw/search?category=67&facet=15616&keyword=%E5%8D%B8%E5%A6%9D&page=0&subcategory=15614']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/search?category=67&facet=15616&keyword=%E5%8D%B8%E5%A6%9D&page=0&subcategory=15614&page=' + str(
            Shopeeremover1Spider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text.replace(',','')
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'Remover'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            i['product_subcategory'] = 'remover'

            yield i

        if Shopeeremover1Spider.page <= 20:
            Shopeeremover1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
