import requests

ip = "*"
url = "http://www.ip-api.com/json/" + ip

response = requests.get(url).json()
if response["status"] == "success":
    print(response)
response = {
    'as': 'AS4847ChinaNetworksInter-Exchange',
    'city': 'Beijing',
    'country': 'China',
    'countryCode': 'CN',
    'isp': 'ChinaNetworksInter-Exchange',
    'lat': 39.9288,
    'lon': 116.3889,
    'org': 'Ritele',
    'query': '*',
    'region': 'BJ',
    'regionName': 'Beijing',
    'status': 'success',
    'timezone': 'Asia/Shanghai',
    'zip': ''
}
