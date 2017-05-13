# -*- encoding: utf-8 -*-
# encoding=utf8
import re
import json
import time
import scrapy

import sqlite3

from pymongo import MongoClient

from amazon_scrapper_fix_4 import VERSION, LOG_DB_NAME

from random_user_agent_module import random_user_agent


class CrawlerProducts(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(CrawlerProducts, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    USER_AGENT = random_user_agent()

    RANDOMIZE_DOWNLOAD_DELAY = True

    name = 'amazon_product'
    allowed_domains = ["amazon.com"]

    start_urls = []

    def parse(self, response):
        #ID (ASIN standard)
        id = re.search("https://www.amazon.com/.*/dp/(.*)", response.url).group(1).encode("utf-8")

        client = MongoClient('localhost', 27017)

        db = client.amazon_products  # Dentro del cliente, hay una base de datos que se llama 'amazon_products'

        item = {}

        if db.products_collection.find({'_id': id}).limit(1).count() == 0:
            try:
                sel = scrapy.Selector(response)

                #Sections (the last section is the actual subsection of the product and the previous one constains the next one and so on
                sects = [re.compile("\\n\s*").sub("", sect).encode("utf-8") for sect in sel.css("#wayfinding-breadcrumbs_feature_div > ul > li > span > a.a-link-normal::text").extract()]
                if not sects:
                    possible_sects = sel.xpath('//*[@id="SalesRank"]/ul/li/span[@class="zg_hrsr_ladder"]')
                    if possible_sects:
                        for sect in possible_sects[0].xpath('./*'):
                            text = sect.xpath('./text()').extract()
                            text = sect.xpath('./a/text()').extract() if not text else text
                            sects.append(text[0].encode("utf-8"))
                    else:
                        sects = [sect.extract("utf-8") for sect in sel.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li/span/a/text()').extract()]

                #Name
                name_contender_1 = sel.css("#productTitle::text")

                if len(name_contender_1) > 0:
                    name_contender_1_aux = re.compile("\\n\s*\\n\s*\\n\s*\\n\s*\\n\s*").sub("", name_contender_1[0].extract())
                    name = re.compile("\\n\s*\\n\s*\\n\s*").sub("", name_contender_1_aux).encode("utf-8")
                else:
                    name = sel.css("#ebooksProductTitle::text")[0].extract().encode("utf-8")

                #Brand
                try:
                    brand = re.compile("\s").sub("", sel.css("#brand::text")[0].extract()).encode("utf-8")
                except:
                    brand = ""

                #Price (sometimes a discount is applied to the original price)
                price_contender_1 = sel.css("#priceblock_ourprice::text").extract()
                price_contender_2 = sel.css("#priceblock_dealprice::text").extract()
                price_contender_3 = sel.css("#priceblock_saleprice::text").extract()
                price_contender_4 = sel.xpath('//*[@id="priceblock_ourprice"]/*/text()').extract()
                price_contender_5 = sel.css('#tmmSwatches > ul > li.swatchElement.selected span.a-color-price::text').extract()
                price_contender_6 = sel.css('span.a-size-medium.a-color-price.header-price::text').extract()
                price_contender_7 = sel.css('#a-autoid-1-announce > span.a-color-base::text').extract()
                price_contender_8 = sel.css('#a-autoid-2-announce > span.a-color-base::text').extract()
                price_contender_9 = sel.css('#a-autoid-0-announce > span.a-color-base > span::text').extract()

                price_string = price_contender_2[0].replace("$", "") if len(price_contender_2) > 0 \
                            else (price_contender_1[0].replace("$", "") if len(price_contender_1) > 0
                                else (price_contender_3[0].replace("$", "") if len(price_contender_3) > 0
                                    else (re.compile("\\n\s*").sub("", price_contender_5[0]).replace("$", "").encode("utf-8") if len(price_contender_5) > 0
                                            else (re.compile("\\n\s*").sub("", price_contender_6[0]).replace("$", "").encode("utf-8") if len(price_contender_6) > 0
                                                  else (re.compile("\\n\s*").sub("", price_contender_7[0]).replace("$", "").replace("from", "").encode("utf-8") if len(price_contender_7) > 0
                                                        else (re.compile("\\n\s*").sub("", price_contender_8[0]).replace("$", "").replace("from", "").encode("utf-8") if len(price_contender_8) > 0
                                                              else (re.compile("\\n\s*").sub("", price_contender_9[0]).replace("$", "").replace("from", "").encode("utf-8")
                                                              )
                                                    )
                                            )
                                    )
                                )
                            ))
                try:
                    try:
                        price = [float(price_string)]
                    except:
                        try:
                            price = [float(price_aux.encode("utf-8")) for price_aux in price_string.split("-")]
                        except:
                            price = [float(price_string.replace(",", ""))]
                except:
                    price_string = (price_contender_4[1] + "." + price_contender_4[2]).encode("utf-8")
                    try:
                        price = [float(price_string)]
                    except:
                        price = [float(price_aux.encode("utf-8")) for price_aux in price_string.split("-")]

                #URL
                url = response.url

                #Recommendations (ASIN ID of recommended products)
                try:
                    people_also_bought = json.loads(sel.xpath('//*[@id="fallbacksession-sims-feature"]/div/@data-a-carousel-options')[0].extract())['ajax']['id_list']
                except:
                    people_also_bought = json.loads(sel.xpath('//*[@id="purchase-sims-feature"]/div/@data-a-carousel-options')[0].extract())['ajax']['id_list']
                people_also_bought = [val.encode("utf-8") for val in people_also_bought]

                #Rate
                try:
                    rate = float(re.search("(\d\.\d*)", sel.css("#acrPopover i > span::text")[0].extract()).group(1))
                except:
                    rate = 0.0

                #Seller
                sold_by_contender_1 = sel.css("#soldByThirdParty > b::text").extract()
                sold_by_contender_2 = sel.css("#merchant-info a::text")
                try:
                    sold_by = sold_by_contender_1[0] if len(sold_by_contender_1) > 0 else (sold_by_contender_2[0].extract() if len(sold_by_contender_2) > 1 else "Amazon.com")
                except:
                    sold_by = ""
                sold_by = sold_by.encode("utf-8")

                #Image
                image = ""
                possible_image_1 = sel.css("#landingImage::attr(src)").extract()
                possible_image_2 = sel.css("#main-image::attr(src)").extract()
                possible_image_3 = sel.css("#imgBlkFront::attr(src)").extract()
                possible_image_4 = sel.css("#ebooksImgBlkFront::attr(src)").extract()

                if not possible_image_1:
                    if not possible_image_2:
                        if not possible_image_3:
                            possible_image_4[0].encode("utf-8")
                        else:
                            possible_image_3[0].encode("utf-8")
                    else:
                        image = possible_image_2[0].encode("utf-8")
                else:
                    image = possible_image_1[0].encode("utf-8")

                #Description located under the price
                description_bullets = sel.css("#feature-bullets ul li span::text").extract()
                description_bullets = [line.encode("utf-8") for line in description_bullets if not line.isspace() and not line == "to make sure this fits."]

                #Product Description
                description_custom_text = ' '.join([val.encode("utf-8") for val in sel.xpath('//*[@id="productDescription"]/div//text()').extract()])

                #Important Information
                important_information_contender1 = ' '.join([val.encode("utf-8") for val in sel.xpath('//*[@id="importantInformation"]/div/div//text()').extract()])
                important_information_contender2 = ' '.join([val.encode("utf-8") for val in sel.xpath('//*[@id="important-information"]/div//text()').extract()])
                important_information = important_information_contender1 if important_information_contender1 != ' ' else important_information_contender2

                #Product Information
                detailed_information = {}
                for row in sel.css("#prodDetails > div tr"):
                    description_title = re.compile("\\n_*").sub("", row.css("th::text")[0].extract().replace(" ", "_").lower()).replace("\t", "").encode("utf-8")
                    description_content = re.compile("\\n\s*").sub("", row.css("td::text")[0].extract()).encode("utf-8")
                    detailed_information[description_title.replace(".", "")] = description_content

                if not any(detailed_information):
                    for row in sel.css('#detail-bullets > table tr > td .content > ul li'):
                        title_list = row.xpath("./b/text()").extract()
                        possible_content = [x for x in row.xpath("./text()").extract() if not x.isspace()]

                        if not all([cont == "," for cont in possible_content]):
                            content_list = possible_content
                        else:
                            content_list = [', '.join([x for x in row.xpath("./a/text()").extract() if not x.isspace()])]

                        if len(title_list) > 0 and len(content_list) > 0:
                            description_title = re.compile("\\n\s*").sub("", title_list[0].replace(": ", "").replace(":", "").lower()).replace(" ", "_").encode("utf-8")
                            description_content = re.compile("\\n\s*").sub("", content_list[0]).encode("utf-8")
                            detailed_information[description_title.replace(".", "")] = description_content

                keys = detailed_information.keys()

                if 'shipping_weight' in keys:
                    detailed_information['shipping_weight'] = detailed_information['shipping_weight'].replace("(", "").encode("utf-8")

                if 'customer_reviews' in keys:
                    del detailed_information['customer_reviews']

                if 'best_sellers_rank' in keys:
                    del detailed_information['best_sellers_rank']

                if 'average_customer_review' in keys:
                    del detailed_information['average_customer_review']

                if 'amazon_best_sellers_rank' in keys:
                    del detailed_information['amazon_best_sellers_rank']

                #Technical Information
                technical_information = {}
                possible_tech_info_1 = sel.css("#technical-details_feature_div tr")

                rows = possible_tech_info_1
                for row in rows:
                    description_title = re.compile("\\n_*").sub("", row.css("th::text")[0].extract().replace(" ", "_").lower()).encode("utf-8")
                    description_content = re.compile("\\n\s*").sub("", row.css("td::text")[0].extract()).encode("utf-8")
                    technical_information[description_title.replace(".", "")] = description_content

                #Size and color combinations (ASIN ID of each possible combination)
                try:
                    size_and_color = json.loads(re.search(re.compile("{.+}", re.MULTILINE), sel.css("[language~=JavaScript]::text")[0].extract()).group(0))['dimensionValuesDisplayData']
                    size_and_color_cleaned = {}
                    for key in size_and_color.keys():
                        size_and_color_cleaned[key.replace(".", "").encode("utf-8")] = [val.encode("utf-8") for val in size_and_color[key]]
                except:
                    size_and_color_cleaned = {}

                #Manufacturer Information
                manufacturer_information = {}
                for row in sel.css(".apm-tablemodule-keyvalue"):
                    try:
                        description_content = re.compile("\\n\s*").sub("", row.css("td.selected span::text")[0].extract()).encode("utf-8")
                    except:
                        manufacturer_information.clear()
                        break
                    description_title = re.compile("\\n_*").sub("", row.css("th span::text")[0].extract().replace(" ", "_").lower()).encode("utf-8")
                    manufacturer_information[description_title.replace(".", "")] = description_content

                #Additional Information
                additional_information = ' '.join(sel.xpath('//*/noscript/div//text()').extract()).encode("utf-8")

                item['_id'] = id
                item['name'] = name
                item['brand'] = brand
                item['price'] = price
                item['url'] = url
                item['recommendation'] = people_also_bought
                item['rate'] = rate
                item['seller'] = sold_by
                item['product_combinations'] = size_and_color_cleaned
                item['image_url'] = image
                item['description_list'] = description_bullets
                item['description_custom_texts'] = description_custom_text
                item['detailed_information'] = detailed_information
                item['timestamp'] = time.time()
                item['sections'] = sects
                item['important_information'] = important_information
                item['technical_information'] = technical_information
                item['manufacturer_information'] = manufacturer_information
                item['additional_information'] = additional_information

                db.products_collection.insert_one(item)
            except:
                log_db_conection = sqlite3.connect(LOG_DB_NAME)
                log_db_cursor = log_db_conection.cursor()

                import traceback
                list = traceback.format_exc().splitlines()
                print list
                limit = len(list)
                error = list[limit - 3].replace("\"", "")

                try:
                    log_db_cursor.execute(
                        "INSERT INTO logT VALUES (\'" + error + "\',\'" + response.url + "\',\'" + str(
                            sects).replace("[", "").replace("]", "").replace(",", "-").replace("'",
                                                                                               "") + "\',\'" + str(
                            VERSION) + "\')")
                except sqlite3.Error:
                    log_db_cursor.execute(
                        "INSERT INTO logT VALUES (\'" + error + "\',\'" + response.url + "\',\'\',\'" + str(
                            VERSION) + "\')")

                log_db_conection.commit()

                log_db_conection.close()

        else:
            pass

        client.close()

        return item



