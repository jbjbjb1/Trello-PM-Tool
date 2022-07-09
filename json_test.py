# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
import pandas as pd

id= "me"
url = f"https://api.trello.com/1/members/{id}/boards"

headers = {
   "Accept": "application/json"
}

query = {
   'key': 'd9ac7eed38f2ff3a3bc03619b897f52e',
   'token': 'b026a238ca833ae69d20245037ac3dc7cb60e3f2b480fd58a7d2a79390d9b6dc'
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
)

data = json.loads(response.text)

with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file,ensure_ascii=False, indent=4)

data1 = response.json()

#df = pd.read_json('output.json', orient='name')
df = pd.DataFrame(data)
df = df = df.loc[:, df.columns.intersection(['name', 'desc', 'closed', 'id'])]
print(df.head())