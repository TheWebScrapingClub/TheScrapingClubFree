import json
import requests

def get_captcha_token(payload_file='payload.txt'):
    url = 'https://api.nextcaptcha.com/createTask'
    with open(payload_file, 'r') as f:
        payload = json.load(f)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        data = response.json()
        status = data.get('status')
        if status == 'ready':
            token = data.get('solution', {}).get('gRecaptchaResponse')
            return token
        elif status == 'pending':
            task_id = data.get('taskId')
            client_key = payload.get('clientKey')
            get_result_url = 'https://api.nextcaptcha.com/getTaskResult'
            poll_payload = {
                "clientKey": client_key,
                "taskId": task_id
            }
            import time
            while True:
                time.sleep(3)
                poll_response = requests.post(get_result_url, headers=headers, json=poll_payload)
                try:
                    poll_response.raise_for_status()
                    poll_data = poll_response.json()
                    poll_status = poll_data.get('status')
                    if poll_status == 'ready':
                        token = poll_data.get('solution', {}).get('gRecaptchaResponse')
                        return token
                    elif poll_status == 'failed':
                        return None
                except Exception as e:
                    return None
        else:
            return None
    except Exception as e:
        return None

def fetch_dns_history(domain='google.com', payload_file='payload.txt'):
    """
    Fetch DNS history using the captcha token from get_captcha_token function
    """
    # Get the captcha token
    token = get_captcha_token(payload_file)
    if not token:
        print("Failed to get captcha token")
        return None
    
    print(f"Got captcha token: {token[:50]}...")
    
    url = "https://completedns.com/dns-history/ajax/"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://completedns.com/dns-history/"
    }
    
    # Prepare the form data with the domain and the captcha token
    data = {
        "domain": domain,
        "token": token
    }
    
    print(f"Making request to {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    try:
        # First, try to get the main page to establish a session
        session = requests.Session()
        main_page = session.get("https://completedns.com/dns-history/")
        print(f"Main page status: {main_page.status_code}")
        
        # Now make the AJAX request
        response = session.post(
            url, 
            headers=headers, 
            data=data,
            allow_redirects=False
        )
        
        # Print response details for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content (first 500 chars): {response.text[:500]}")
        
        response.raise_for_status()
        
 
        print(f"Full response content: {response.text}")
        

        
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching DNS history: {e}")
        return None

# Example usage
if __name__ == "__main__":
    result = fetch_dns_history("google.com")
    if result:
        print("DNS History Result:", result)
    else:
        print("Failed to fetch DNS history")