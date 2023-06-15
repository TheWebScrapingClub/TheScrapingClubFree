from w3lib.http import basic_auth_header 

class CustomProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta["proxy"] = "http://browser.webit.live:8888"
		request.headers["Proxy-Authorization"] = basic_auth_header("USER", "PWD")
