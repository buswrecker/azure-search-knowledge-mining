import requests

url = "https://kmopenhacksearchservice.search.windows.net/indexes/openhack-jl-index/docs/search?api-version=2019-05-06"

payload = "{  \r\n     \"count\": true,\r\n     \"search\": \"London+\\\"Buckingham Palace\\\"\",  \r\n     \"select\": \"file_name, url, size, last_modified\"\r\n}  "
headers = {
  'api-key': 'F65343057B0C61194591A35C44D48CD4',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
