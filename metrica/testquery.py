import requests

data = {
    "metric": 1,
    "product": 1,
    "timestamp": 5,
    "value": 4
}

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

url = "http://localhost:8000/appmetrica/submit/"

# rq = requests.post(url, json=data)
rq = requests.get(url)
print(rq.text)
