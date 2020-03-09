# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup


class Shopeeeyeshadow1Spider(scrapy.Spider):
    name = 'shopeeeyeshadow1'

    start_urls = ['https://shopee.tw/search?category=67&facet=15722&keyword=%E7%9C%BC%E5%BD%B1&page=0&subcategory=15701']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/search?category=67&facet=15722&keyword=%E7%9C%BC%E5%BD%B1&page=0&subcategory=15701&page=' + str(
            Shopeeeyeshadow1Spider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'EyeShadow'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            yield i

        if Shopeeeyeshadow1Spider.page <= 100:
            Shopeeeyeshadow1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
