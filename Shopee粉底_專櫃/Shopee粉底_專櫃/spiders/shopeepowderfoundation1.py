# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopeeItem
from bs4 import BeautifulSoup

class Shopeepowderfoundation1Spider(scrapy.Spider):
    name = 'shopeepowderfoundation1'

    start_urls = ['https://shopee.tw/search?category=67&facet=15710&keyword=%E7%B2%89%E5%BA%95%E3%80%81%E6%B0%A3%E5%A2%8A%E7%B2%89%E9%A4%85&page=0&subcategory=15701']

    page = 1

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        i = ShopeeItem()
        all_products = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
        next_page = 'https://shopee.tw/search?category=67&facet=15710&keyword=%E7%B2%89%E5%BA%95%E3%80%81%E6%B0%A3%E5%A2%8A%E7%B2%89%E9%A4%85&page=0&subcategory=15701&page=' + str(
            Shopeepowderfoundation1Spider.page)

        for product in all_products:
            img = []
            i['product_name'] = product.find("div", {'class': '_1NoI8_ _16BAGk'}).text
            i['product_price'] = product.find("span", class_="_341bF0").text
            i['product_url'] = 'https://shopee.tw' + product.a['href']
            i['product_category'] = 'Foundation'
            image = product.find('img').attrs['src']
            img.append(image)
            i['product_images'] = img[0]
            i['product_source'] = "Shopee"
            yield i

        if Shopeepowderfoundation1Spider.page <= 100:
            Shopeepowderfoundation1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
