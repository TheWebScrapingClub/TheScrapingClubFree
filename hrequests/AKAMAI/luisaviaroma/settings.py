# -*- coding: utf-8 -*-

# Scrapy settings for luisaviaroma project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Googlebot'

SPIDER_MODULES = ['luisaviaroma.spiders']
NEWSPIDER_MODULE = 'luisaviaroma.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
FIELDS_TO_EXPORT = ['productcode', 'gender', 'fullprice', 'price', 'currency', 'country', 'itemurl', 'brand', 'website', 'competence_date', 'pricemax']
CSV_DELIMITER = "|"
#CONCURRENT_REQUESTS = 3
FEED_EXPORTERS = {
    'csv': 'luisaviaroma.csv_item_exporter.MyProjectCsvItemExporter',
}


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

#HTTP_PROXY = 'https://95.158.128.189:8080'

# Enable or disable downloader middlewares
#DOWNLOADER_MIDDLEWARES = {
#    'luisaviaroma.middlewares.ProxyMiddleware': 410,
#}


# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 408, 502, 407]


# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
#BASEPATH='/re/pricing/retail/Proxies/'


# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings


# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = "http://lum-customer-re_analytics-zone-staticresidentialszone:m2ihyxm9l3wq@zproxy.lum-superproxy.io:22225"


#42.104.84.107:8080
#42.104.84.109:8080
#89.236.17.106:3128
#61.216.96.43:8081
#147.75.113.108:8080
#52.164.249.198:3128
#13.92.196.150:8080
#45.77.247.164:8080
#1.55.76.142:6868
#154.119.50.246:53281
#159.89.195.153:8118
#47.206.51.67:8080
#117.6.161.118:53281
#82.147.116.201:41234
#195.201.7.153:80
#186.46.90.50:53281
#122.183.243.68:8080
#159.224.176.205:53281
#46.254.217.54:53281

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
COOKIES_DEBUG=True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'luisaviaroma.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'luisaviaroma.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'luisaviaroma.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
