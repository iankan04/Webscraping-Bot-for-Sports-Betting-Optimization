import requests
import random

def get_proxies():
    proxy_url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"

    req = requests.get(proxy_url)
    proxies = req.text.split('\n')

    return proxies

def get_random_proxy(proxies):
    return {"https" : random.choice(proxies)}

def get_working_proxies():
    working = []
    i = 0
    while i < len(get_proxies()):
        proxy = get_random_proxy(get_proxies())
        print(f"using {proxy}...")
        try:
            req = requests.get("https://www.google.com/", proxies=proxy, timeout=3)
            print(req.status_code)
            if req.status_code==200:
                working.append(proxy)
                return working
        except:
            pass
    return "No working proxy found :("

global proxy
proxy = random.choice(get_working_proxies())