import requests

data = {
    "metric": 2,
    "product": 1,
    "timestamp": 6,
    "value": 7
}

'''
data = {
    "metric": 1,
    "product": 1,
    "values": [
        {
            "timestamp": 5,
            "value": 5,
        },
        {
            "timestamp": 5,
            "value": 5,
        }
    ]
}
'''

url = "http://localhost:8000/appmetrica/submit/"

ssn = requests.Session()
'''
rq = ssn.get(url)
# rq_cookies = rq.cookies.get_dict()
res = rq.text.split()
token = ""
for item in res:
    if item.startswith("value="):
        token = item[item.find('\"')+1:-2]
        break
        # print(item, token)

# data["csrfmiddlewaretoken"] = token
'''
rq2 = ssn.post(url, data=data)
print(rq2.text)
# print(res)

'''
POST /appmetrica/submit/ HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: csrftoken=w311gn4NFHrqJWPk6dlsBGhWD0DNKAwd
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
metric: 1
product: 1
timestamp: 5
value: 4
Origin: http://localhost:8000
Pragma: no-cache
Cache-Control: no-cache
Content-Length: 0
'''

'''
HTTP/1.1 500 Internal Server Error
Date: Wed, 24 Apr 2024 07:59:53 GMT
Server: WSGIServer/0.2 CPython/3.11.7
Content-Type: text/html; charset=utf-8
X-Frame-Options: DENY
Content-Length: 73232
Vary: Cookie
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
'''