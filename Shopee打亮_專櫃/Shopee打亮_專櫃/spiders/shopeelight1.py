# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup


class Shopeelight1Spider(scrapy.Spider):
    name = 'shopeelight1'

    start_urls = ['https://shopee.tw/search?category=67&facet=15720&keyword=%E6%89%93%E4%BA%AE%E3%80%81%E4%BF%AE%E5%AE%B9&page=0&subcategory=15701']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/search?category=67&facet=15720&keyword=%E6%89%93%E4%BA%AE%E3%80%81%E4%BF%AE%E5%AE%B9&page=0&subcategory=15701&page=' + str(
            Shopeelight1Spider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text.replace(',','')
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'Blush'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            i['product_subcategory'] = 'trim'

            yield i

        if Shopeelight1Spider.page <= 20:
            Shopeelight1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
