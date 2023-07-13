import os
import random
from scrapy import signals
from scrapy.utils.project import get_project_settings
import re
import random
import base64
import logging
import boto3
import json



class ProxyMiddleware(object):

	def process_request(self, request, spider):
		settings = get_project_settings()
		request.meta['proxy'] = settings.get('HTTP_PROXY')
	

log = logging.getLogger('scrapy.proxies')


class Mode:
	RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)


class RandomProxy(object):
	def logtotable(self):
		settings = get_project_settings()
		self.website = settings.get('WEBSITE')
		self.instanceid = settings.get('ISTANCEID')
		
		lambda_client = boto3.client('lambda')

		log_event = {
			"source_code": "PROXY", 
			"phase_code": "SATELLITE",
			"message_type_code": "100",
			"message": "Proxy not able to run spider until the end of execution",
			"instance_code": self.instanceid,
			"measure1": "0",
			"measure2": "0",
			"measure3": self.website,
			"measure4": "0",
			"measure5": "0",
			"measure6": "0",
			"measure7": "0",
			"measure8": "0",
			"measure9": "0",
			"measure10": "0",
		}

		response = lambda_client.invoke(
		  FunctionName='WriteSourcingLog',
		  Payload=json.dumps(log_event),
		)
		
		
	def __init__(self, settings):
		self.mode = settings.get('PROXY_MODE')
		self.proxy_list = settings.get('PROXY_LIST')
		self.chosen_proxy = ''
		self.mode=int(self.mode)
		if self.mode != -1:
			if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
				if self.proxy_list is None:
					raise KeyError('PROXY_LIST setting is missing')
				self.proxies = {}
				fin = open(self.proxy_list)
				try:
					for line in fin.readlines():
						parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', line.strip())
						if not parts:
							continue

						# Cut trailing @
						if parts.group(2):
							user_pass = parts.group(2)[:-1]
						else:
							user_pass = ''

						self.proxies[parts.group(1) + parts.group(3)] = user_pass
				finally:
					fin.close()
				if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
					self.chosen_proxy = random.choice(list(self.proxies.keys()))
			elif self.mode == Mode.SET_CUSTOM_PROXY:
				custom_proxy = settings.get('CUSTOM_PROXY')
				self.proxies = {}
				parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', custom_proxy.strip())
				if not parts:
					raise ValueError('CUSTOM_PROXY is not well formatted')

				if parts.group(2):
					user_pass = parts.group(2)[:-1]
				else:
					user_pass = ''

				self.proxies[parts.group(1) + parts.group(3)] = user_pass
				self.chosen_proxy = parts.group(1) + parts.group(3)

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings)

	def process_request(self, request, spider):
		if self.mode != -1:
			# Don't overwrite with a random one (server-side state for IP)
			if 'proxy' in request.meta:
				print ("process_request")
				print (request.meta)
				if request.meta["exception"] is False and 'retry_times' in request.meta:
					if request.meta["retry_times"] > 5:
						request.meta["exception"] = True
						return
					else:
						return
			request.meta["exception"] = False
			if len(self.proxies) == 0:
				#self.logtotable()
				raise ValueError('All proxies are unusable, cannot proceed')

			if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
				proxy_address = random.choice(list(self.proxies.keys()))
			else:
				proxy_address = self.chosen_proxy

			proxy_user_pass = self.proxies[proxy_address]

			if proxy_user_pass:
				request.meta['proxy'] = proxy_address
				basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
				request.headers['Proxy-Authorization'] = basic_auth
			else:
				request.meta['proxy'] = proxy_address
				log.debug('Proxy user pass not found')
			log.debug('Using proxy <%s>, %d proxies left' % (proxy_address, len(self.proxies)))

	def process_exception(self, request, exception, spider):
		if 'proxy' not in request.meta:
			return
		if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
			proxy = request.meta['proxy']
			try:
				del self.proxies[proxy]
			except KeyError:
				pass
			request.meta["exception"] = True
			if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
				self.chosen_proxy = random.choice(list(self.proxies.keys()))
			log.info('Removing failed proxy <%s>, %d proxies left' % (
				proxy, len(self.proxies)))
