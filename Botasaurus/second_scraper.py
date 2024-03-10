from botasaurus import *

@request(use_stealth=True)
def scrape_heading_task(request: AntiDetectRequests, data):
    response = request.get('https://www.omkar.cloud/')
    print(response.status_code)
    return response.text

scrape_heading_task()
     
