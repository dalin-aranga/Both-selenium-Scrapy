from selenium import webdriver
import scrapy
from scrapy.selector import Selector
import time


class Crasdetails(scrapy.Spider):
    name = 'carsdetails'
    driver = webdriver.Firefox()
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            'Model',
            'Version',
            'Price',
            'Image',
            'Use Length',
            'Buy Date',
            'Power',
            'Comfort & Convenience',
            'Extra',
            'Safety & Security',
            'Description',
            'Color',
            'Body',
            'Doors',
            'Seats',
            'Displacement',
            'Gear Type',
            'Gears',
            'Clinders',
            'Weight',
            'Seler Type',
            'Seler Telephone',
            'Seler City',
            'Seler Country',
            'Seler Map Link',
            'Url'

        ]
    };

    def start_requests(self):
        urls = []
        for i in range(1, 21):
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=A&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=B&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=D&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=E&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=F&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=I&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=L&atype=C&')
            urls.append('https://www.autoscout24.com/lst/?sort=price&desc=0&offer=J%2CU%2CO%2CD&ustate=N%2CU&size=20&page=' + str(i) + '&cy=N&atype=C&')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(3)

        page_sourse = Selector(text=self.driver.page_source)
        vehicle_link = page_sourse.xpath('//a[@data-item-name="detail-page-link"]/@href').extract()
        for vehicle_a in vehicle_link:
            real_vehicle_link = 'https://www.autoscout24.com'+vehicle_a
            yield scrapy.Request(url=real_vehicle_link,callback=self.details)

    def details(self,response):
        url = response.url
        self.driver.get(response.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(3)
        page_sourse = Selector(text=self.driver.page_source)
        price = page_sourse.xpath('//div[@class ="cldt-price "]/h2/text()').extract_first()
        seler_type = page_sourse.xpath('//h3[@class="sc-font-bold sc-font-m"]/text()').extract_first()
        sele_tele = page_sourse.xpath('//a[@data-type="callLink"]/text()').extract_first()
        sele_ad = page_sourse.xpath('//div[@data-item-name="vendor-contact-city"]/text()').extract_first()
        sele_c = page_sourse.xpath('//div[@data-item-name="vendor-contact-country"]/text()').extract_first()
        sele_map = page_sourse.xpath('//a[@class="cldt-open-map sc-btn-ross"]/@href').extract_first()
        image = page_sourse.xpath('//img[@class="gallery-picture__image"]/@src').extract()
        model = page_sourse.xpath('//span[@class="cldt-detail-makemodel sc-ellipsis"]/text()').extract_first()
        version = page_sourse.xpath('//span[@class="cldt-detail-version sc-ellipsis"]/text()').extract_first()
        use_length = page_sourse.xpath('//span[@class="sc-font-l cldt-stage-primary-keyfact"]/text()').extract_first()
        try:
            buy_date = page_sourse.xpath('//span[@class="sc-font-l cldt-stage-primary-keyfact"]/text()')[1].extract()
        except:
            buy_date = ''
        try:
            power = page_sourse.xpath('//span[@class="sc-font-l cldt-stage-primary-keyfact"]/text()')[2].extract()
        except:
            power = ''
        description = page_sourse.xpath('//div[@data-type="description"]/text()').extract()
        try:
            comfort_convenience = page_sourse.xpath('//div[@class="cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left"][1]/span/text()').extract()
        except:
            comfort_convenience = ''
        try:
            extras = page_sourse.xpath('//div[@class="cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left"][2]/span/text()').extract()
        except:
            extras = ''
        try:
            safety_security = page_sourse.xpath('//div[@class="cldt-equipment-block sc-grid-col-3 sc-grid-col-m-4 sc-grid-col-s-12 sc-pull-left"][3]/span/text()').extract()
        except:
            safety_security = ''
        colour = page_sourse.xpath('//dt[contains(text(),"Body Color")]/following-sibling::dd[1]/a/text()').extract_first()
        body = page_sourse.xpath('//dt[contains(text(),"Body")]/following-sibling::dd[2]/a/text()').extract_first()
        try:
            doors = page_sourse.xpath('//dt[contains(text(),"Nr. of Doors")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            doors= ''
        try:
            seat = page_sourse.xpath('//dt[contains(text(),"Nr. of Seats")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            seat =''
        try:
            displacement = page_sourse.xpath('//dt[contains(text(),"Displacement")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            displacement =''
        try:
            gear_type = page_sourse.xpath('//dt[contains(text(),"Gearing Type")]/following-sibling::dd[1]/a/text()').extract_first()
        except:
            gear_type =''
        try:
            gears = page_sourse.xpath('//dt[contains(text(),"Gears")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            gears = ''
        try:
            clinder = page_sourse.xpath('//dt[contains(text(),"Cylinders")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            clinder = ''
        try:
            weight = page_sourse.xpath('//dt[contains(text(),"Weight")]/following-sibling::dd[1]/text()').extract_first().strip()
        except:
            weight= ''

        yield {
            'Model': model,
            'Version': version,
            'Price': price,
            'Image': image,
            'Use Length': use_length,
            'Buy Date': buy_date,
            'Power': power,
            'Comfort & Convenience': comfort_convenience,
            'Extra': extras,
            'Safety & Security': safety_security,
            'Description': description,
            'Color': colour,
            'Body': body,
            'Doors': doors,
            'Seats': seat,
            'Displacement': displacement,
            'Gear Type': gear_type,
            'Gears': gears,
            'Clinders': clinder,
            'Weight': weight,
            'Seler Type': seler_type,
            'Seler Telephone': sele_tele,
            'Seler City': sele_ad,
            'Seler Country': sele_c,
            'Seler Map Link': sele_map,
            'Url': url
        }












