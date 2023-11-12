# -*- coding: utf-8 -*-
import re, ast  
import datetime
from scrapy import Request, Spider
from luisaviaroma.items import LuisaviaromaItem

class RadarSpider(Spider):
    name = "radar"
    allowed_domains = ["luisaviaroma.com"]
    start_urls = (
        'http://www.luisaviaroma.com/',
    )
    locations_file = open('locations.txt')
    
    COUNTRIES = locations_file.readlines()
    categories_file = open('categories.txt')
    CATEGORIES = categories_file.readlines()
    def start_requests(self):
        for i, countrycurrency in enumerate(self.COUNTRIES):
            country, currency=countrycurrency.split(',')
            for url in self.CATEGORIES:
                new_url=url.replace('it/', country.strip()+'/')
                string='LVR_UserData=Ver=6&cty='+country.upper().strip()+'&curr='+currency.strip()+'&lang=EN; '
                print(string)
                meta = {'cookiejar': i}
                meta['country'] = country
                meta['string'] = string
                cookies = {'LVR_UserData': "cty={}&lang=EN".format(country)}
                if '/kids-boys' in url:
                    meta['gender'] = 'Boys'
                elif '/kids-girls' in url:
                    meta['gender'] = 'Girls'                
                elif '/men' in url:
                    meta['gender'] = 'Men'                
                elif '/women' in url:
                    meta['gender'] = 'Women'
                yield Request(new_url.strip(), callback=self.parse_product, meta=meta, headers={'referer':'https://www.google.com/', 'authority': 'www.luisaviaroma.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'dnt':'1',  'cookie': string+'LVR_User=ver=1; LVR_TRACKING=9922498e-bc1b-4544-9314-c18ce7fc38db; _dy_c_exps=; _dy_c_att_exps=; LVR_MarketingCookies=true; LVR_AnalyticsCookies=true; LVR_BC=viewed; _ga=GA1.2.1708709272.1537438902; _dyid=-6656320097445772515; _dycnst=dg; TCID=20189412214411851862611; tinytrckr=qvqd8bw0v3r5edo5o4mm9; LVR_FT=viewed; _gcl_au=1.1.768511949.1538640150; cto_lwid=ee355189-7655-494d-b098-b6743a7eab66; ASP.NET_SessionId=isajkttwp4eawsdifzcbnng0; _dy_csc_ses=t; _dyjsession=de16ad77e808b6c89409ab73eac9f466; TCSESSION=201810111321611397843738; scarab.mayAdd=%5B%7B%22i%22%3A%2268I05C014-MDk50%22%7D%5D; scarab.visitor=%2237F77EB2FED1F6B1%22; _abck=7E1314E0493C108DC9CF0891270270275F65B514F76B0000B174A35B83CAF83B~0~ZpLHRRGPiYVAB1TWH1aOULyzbGpsY6UrAKd5Lup6fhM=~-1~-1; tc_cj_v2=%5Ecl_%5Dny%5B%5D%5D_mmZZZZZZKONMROMRSJQLPZZZ%5D; bm_sz=B2E9885800D90204BF92CB596384133B~QAAQXnJlX5lQ5kRnAQAAz/xFjQ/XOeVl4bADKMmUD+/Dng1G+KN9PrLi2ugwnfFGNQ7e7FEBLDUDTlypdn4rkaZ9f3oStG056Fg9HHzDcyB4uMTqp5rnopd8HSpIEJ6SbRqlYzVUYISk63ZdvQGDkhxpaOY+csV6PcnrhM9WXFHitEiO2f4WgaKoQpquXGYzNIhubIE=; LVR_Ref=faurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL1VzZXJTZXNzaW9uLmFzcHg/aW5teWFyZWE9RmFsc2UmaW5zaG9wcGluZ2JhZz1GYWxzZSZ2PTIwMTgwOTIwMTA0Mg==&laurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL2VuLWNvLz9ha2FfcmU9MQ==&fadate=2018-09-20 12:21:39&ladate=2018-12-08 11:03:54&faip=2.32.213.191&laip=87.2.210.217; bm_mi=1BA77947D3459384CFDA6A0FC701150C~orinP6d9qO+JNcxrfS1zcK8t6C+nEgdwF1uHqAV7Kykf4dOC/zaGWIrgDCCU0M3jPJyCrtguUht1YPygpIrqN9TBzu8efJFmcnwZuhq/Ju7Cae/myCohJG+JyApPYxWrBq4i+rEwhnGAd50L9Ag8yAFb4IwWifrt7INA5hryYoED/lBwsqA7qA4iSmA8MWNAFq8nEwrBKvvIIZ4FU8JNViLimw2EWj9gWpfpSDLQoxaVeOMp9m6oPaeHMIA1qQYNRoJsoe72V5i8tOHUKzmdR+BqzVD5XI+VjfQYmlhqZN8=; _dy_geo=IT.EU.IT_09.IT_09_Milan; _dy_df_geo=Italy..Milan; _dy_toffset=0; _gid=GA1.2.2037067497.1544263439; ak_bmsc=B365718A485AD5A8ED69C77AB8DFFDD25F65725E267D000009970B5C2A7EA944~plf+6ON5qXAsm9NjERFvJwHbQcs3Am7nARUwmHNXlFQhS+6UWFFfvMnHE4sZxzXptTf99yS5LBeGrxK7fOMo1Imnv/MeLjcrtsy5AJGrJoCNnVQGQzPpVmNVfGeHL7scmNMESnqpywH6ytZ6TAc28/DEWKg1JFzeYmhR+586/XS837Xp/4H6AEi45WRPwOfvyxW9kn0F9AqdxjueupyzixTQ09wnSjTYFoBP/F3bbKk3Ohofui8eCZys6zKJPdoW50; _fbp=fb.1.1544263440887.1964151672; _dy_ses_load_seq=73460%3A1544263612149; _dy_soct=351053.575000.1544263437*246797.371038.1544263612*246798.371039.1544263612*246799.371040.1544263612*246800.371041.1544263612*319900.511043.1544263612*135768.190303.1544263612; _dycst=dk.m.c.ss.frv5.ltos.ah.clk.; _dyus_8767529=4484%7C1810%7C32%7C0%7C0%7C0.0.1483965215823.1544263612672.60298396.0%7C341%7C49%7C11%7C1171%7C280%7C0%7C0%7C0%7C0%7C0%7C0%7C280%7C0%7C0%7C0%7C0%7C0%7C280%7C19%7C2%7C0%7C0%7C0; tc_scoring_pv=243; _gat=1; LVR_Touchpoint=url=/en-co/widget.css.map$query=$referrer=; bm_sv=F3208D65374448EE99B44B95AA680DBD~x+oBps1Vs6+O3KII2XWHM1kZ16oFqRhXeYx8Iinn2F2TJB3iKHGdb61uUciODlyJvC1KIT3MmwnEFkU8i03YxlffBtqKklXJ52JfNCRNbPs8CFoIsWJcR2EufcOejzSeOVxsUyo9XgMnhegUaNxwC2vG47FbVU4X+EvOxhrrOrE=; stc114797=env:1544263439%7C20190108100359%7C20181208103655%7C2%7C1043009:20191208100655|uid:1537438904343.44532291.32420635.114797.1123380068.:20191208100655|srchist:1043009%3A1544263439%3A20190108100359:20191208100655|tsa:1544263439604.69089039.91262674.40529623082002186.:20181208103655; RT="dm=www.luisaviaroma.com&si=9965b570-8db0-43b7-838e-fb8c9b3bde02&ss=1544263433114&sl=3&tt=17529&obo=0&sh=1544263618784%3D3%3A0%3A17529%2C1544263442745%3D2%3A0%3A9540%2C1544263434685%3D1%3A0%3A1082&bcn=%2F%2F364bf52c.akstat.io%2F&ld=1544263618785&r=https%3A%2F%2Fwww.luisaviaroma.com%2Fen-co%2F%3Faka_re%3D1&ul=1544263620659"'}, dont_filter=True)

    def parse_product(self, response):
        #print response.text
            
        item = LuisaviaromaItem()
        products = response.xpath('//div[@itemprop="itemListElement"]')
        for product in products:
            item['productcode'] = product.xpath('(./a[@class="article__inner"]/@href)').re('[A-Z\d]{3}-[A-Z\d]{6}')
            item['gender'] = response.meta.get('gender')
            item['fullprice'] = product.xpath(
                '*//span[@class="discount_container catalog__item__price__inner"]/span/text()').re(
                '[\d\.\,]+')[0] if product.xpath(
                '*//span[@class="discount_container catalog__item__price__inner"]/span/text()').re(
                '[\d\.\,]+') else ''
            item['price'] = product.xpath(
                '*//span[contains(@class, "catalog__item__price__info")]/span/text()').re(
                '[\d\.\,]+')[0] if product.xpath(
                '*//span[contains(@class, "catalog__item__price__info")]/span/text()').re(
                '[\d\.\,]+') else ''
            price = product.xpath('*//span[contains(@class, "catalog__item__price__info")]/span/text()').extract()[0] if product.xpath(
                '*//span[contains(@class, "catalog__item__price__info")]/span/text()').re(
                '[\d\.\,]+') else ''

            item['currency'] = re.sub('\d?,?\.?\s?','',price).strip() if price else ''
            item['country'] = response.meta.get('country').replace('\n', '').upper()
            try:
                item['itemurl'] = response.urljoin(product.xpath('(./a[@class="article__inner"]/@href)').extract()[0])
            except:
                pass
            item['brand'] = product.xpath(
                '*//span[@class="catalog__item__brand"]/span/text()').extract()
            item['website'] = 'LUISAVIAROMA'
            item['competence_date'] = datetime.datetime.today().strftime('%Y%m%d')
            item['pricemax'] = 0
            yield item
            
        currentpage = int(response.xpath('//div/@data-currentpage').extract()[0])
        totalpage = int(response.xpath('//div/@data-totalpages').extract()[0])
        print "totalpage"
        print totalpage
        print "currentpage"
        print currentpage
        print response.headers
        if currentpage <= totalpage:
            baseurl, pagenum=response.url.split('Page=')
            currentpage=currentpage+1
            url=baseurl + 'Page=' + str(currentpage)
            yield Request(url,
                callback=self.parse_product,
                meta=response.meta,
                dont_filter=True, 
                headers={'referer':'https://www.google.com/', 'authority': 'www.luisaviaroma.com', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'dnt':'1',  'cookie': response.meta.get('string')+'LVR_User=ver=1; LVR_TRACKING=9922498e-bc1b-4544-9314-c18ce7fc38db; _dy_c_exps=; _dy_c_att_exps=; LVR_MarketingCookies=true; LVR_AnalyticsCookies=true; LVR_BC=viewed; _ga=GA1.2.1708709272.1537438902; _dyid=-6656320097445772515; _dycnst=dg; TCID=20189412214411851862611; tinytrckr=qvqd8bw0v3r5edo5o4mm9; LVR_FT=viewed; _gcl_au=1.1.768511949.1538640150; cto_lwid=ee355189-7655-494d-b098-b6743a7eab66; ASP.NET_SessionId=isajkttwp4eawsdifzcbnng0; _dy_csc_ses=t; _dyjsession=de16ad77e808b6c89409ab73eac9f466; TCSESSION=201810111321611397843738; scarab.mayAdd=%5B%7B%22i%22%3A%2268I05C014-MDk50%22%7D%5D; scarab.visitor=%2237F77EB2FED1F6B1%22; _abck=7E1314E0493C108DC9CF0891270270275F65B514F76B0000B174A35B83CAF83B~0~ZpLHRRGPiYVAB1TWH1aOULyzbGpsY6UrAKd5Lup6fhM=~-1~-1; tc_cj_v2=%5Ecl_%5Dny%5B%5D%5D_mmZZZZZZKONMROMRSJQLPZZZ%5D; bm_sz=B2E9885800D90204BF92CB596384133B~QAAQXnJlX5lQ5kRnAQAAz/xFjQ/XOeVl4bADKMmUD+/Dng1G+KN9PrLi2ugwnfFGNQ7e7FEBLDUDTlypdn4rkaZ9f3oStG056Fg9HHzDcyB4uMTqp5rnopd8HSpIEJ6SbRqlYzVUYISk63ZdvQGDkhxpaOY+csV6PcnrhM9WXFHitEiO2f4WgaKoQpquXGYzNIhubIE=; LVR_Ref=faurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL1VzZXJTZXNzaW9uLmFzcHg/aW5teWFyZWE9RmFsc2UmaW5zaG9wcGluZ2JhZz1GYWxzZSZ2PTIwMTgwOTIwMTA0Mg==&laurl=aHR0cDovL3d3dy5sdWlzYXZpYXJvbWEuY29tL2VuLWNvLz9ha2FfcmU9MQ==&fadate=2018-09-20 12:21:39&ladate=2018-12-08 11:03:54&faip=2.32.213.191&laip=87.2.210.217; bm_mi=1BA77947D3459384CFDA6A0FC701150C~orinP6d9qO+JNcxrfS1zcK8t6C+nEgdwF1uHqAV7Kykf4dOC/zaGWIrgDCCU0M3jPJyCrtguUht1YPygpIrqN9TBzu8efJFmcnwZuhq/Ju7Cae/myCohJG+JyApPYxWrBq4i+rEwhnGAd50L9Ag8yAFb4IwWifrt7INA5hryYoED/lBwsqA7qA4iSmA8MWNAFq8nEwrBKvvIIZ4FU8JNViLimw2EWj9gWpfpSDLQoxaVeOMp9m6oPaeHMIA1qQYNRoJsoe72V5i8tOHUKzmdR+BqzVD5XI+VjfQYmlhqZN8=; _dy_geo=IT.EU.IT_09.IT_09_Milan; _dy_df_geo=Italy..Milan; _dy_toffset=0; _gid=GA1.2.2037067497.1544263439; ak_bmsc=B365718A485AD5A8ED69C77AB8DFFDD25F65725E267D000009970B5C2A7EA944~plf+6ON5qXAsm9NjERFvJwHbQcs3Am7nARUwmHNXlFQhS+6UWFFfvMnHE4sZxzXptTf99yS5LBeGrxK7fOMo1Imnv/MeLjcrtsy5AJGrJoCNnVQGQzPpVmNVfGeHL7scmNMESnqpywH6ytZ6TAc28/DEWKg1JFzeYmhR+586/XS837Xp/4H6AEi45WRPwOfvyxW9kn0F9AqdxjueupyzixTQ09wnSjTYFoBP/F3bbKk3Ohofui8eCZys6zKJPdoW50; _fbp=fb.1.1544263440887.1964151672; _dy_ses_load_seq=73460%3A1544263612149; _dy_soct=351053.575000.1544263437*246797.371038.1544263612*246798.371039.1544263612*246799.371040.1544263612*246800.371041.1544263612*319900.511043.1544263612*135768.190303.1544263612; _dycst=dk.m.c.ss.frv5.ltos.ah.clk.; _dyus_8767529=4484%7C1810%7C32%7C0%7C0%7C0.0.1483965215823.1544263612672.60298396.0%7C341%7C49%7C11%7C1171%7C280%7C0%7C0%7C0%7C0%7C0%7C0%7C280%7C0%7C0%7C0%7C0%7C0%7C280%7C19%7C2%7C0%7C0%7C0; tc_scoring_pv=243; _gat=1; LVR_Touchpoint=url=/en-co/widget.css.map$query=$referrer=; bm_sv=F3208D65374448EE99B44B95AA680DBD~x+oBps1Vs6+O3KII2XWHM1kZ16oFqRhXeYx8Iinn2F2TJB3iKHGdb61uUciODlyJvC1KIT3MmwnEFkU8i03YxlffBtqKklXJ52JfNCRNbPs8CFoIsWJcR2EufcOejzSeOVxsUyo9XgMnhegUaNxwC2vG47FbVU4X+EvOxhrrOrE=; stc114797=env:1544263439%7C20190108100359%7C20181208103655%7C2%7C1043009:20191208100655|uid:1537438904343.44532291.32420635.114797.1123380068.:20191208100655|srchist:1043009%3A1544263439%3A20190108100359:20191208100655|tsa:1544263439604.69089039.91262674.40529623082002186.:20181208103655; RT="dm=www.luisaviaroma.com&si=9965b570-8db0-43b7-838e-fb8c9b3bde02&ss=1544263433114&sl=3&tt=17529&obo=0&sh=1544263618784%3D3%3A0%3A17529%2C1544263442745%3D2%3A0%3A9540%2C1544263434685%3D1%3A0%3A1082&bcn=%2F%2F364bf52c.akstat.io%2F&ld=1544263618785&r=https%3A%2F%2Fwww.luisaviaroma.com%2Fen-co%2F%3Faka_re%3D1&ul=1544263620659"'}
                )
