import requests

url = 'http://localhost:5000/detect'
#payload = {"flag":"0"}
#response = requests.put(url, params=payload)
response = requests.get(url)
print(response.text)