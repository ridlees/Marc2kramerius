import requests as r
import json

def escape(uuid):
	return uuid.replace(':','\:').replace('-','\-')

"""
url = "https://kramerius.mzk.cz/search/api/v5.0/search?q=issn:1802-6265&fl=*&rows=100000000&wt=json"

response = r.get(url).json()
print(len(response.get("response").get("docs")))
with open("data.json", "w") as outfile:
    json.dump(response, outfile)
"""

url2 = "https://www.ndk.cz/search/api/v5.0/search?q=issn:1802-6265&fl=*&rows=10000&wt=json"
session = r.Session()
response = session.get(url2, stream=True).json()
docs = response.get("response").get("docs")
print(len(docs))
print(docs[0])
with open("dump.json", "w") as outfile:
    json.dump(response, outfile)

PID = docs[0].get("root_pid")
print(PID)
data = []
for i in range(0,10):
        slicer = i*27500
        response = session.get(f"https://www.ndk.cz/search/" + "api/v5.0/search?q=root_pid:" + escape(PID)+f"&fl=*&rows=27500&start={slicer}&wt=json", stream=True)
        response.raise_for_status()
        response = response.json()
        data.append(response)
print(len(data))
with open("PID.json", "w") as outfile:
        json.dump(response, outfile)
        docs = response.get("response").get("docs")
        print(len(docs))
        


