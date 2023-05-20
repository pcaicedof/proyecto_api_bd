import requests
 
def send_payload(payload, url):
    response = requests.post(url, json=payload)
    print(response)
    return response