# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup

class ShopeetoolsSpider(scrapy.Spider):
    name = 'shopeetools'
    start_urls = ['https://shopee.tw/%E7%BE%8E%E5%AE%B9%E5%B7%A5%E5%85%B7-cat.67.1557']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/%E7%BE%8E%E5%AE%B9%E5%B7%A5%E5%85%B7-cat.67.1557?page=' + str(
            ShopeetoolsSpider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text.replace(',','')
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'MakeupTools'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            i['product_subcategory'] = 'makeuptools'

            yield i

        if ShopeetoolsSpider.page <= 20:
            ShopeetoolsSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
