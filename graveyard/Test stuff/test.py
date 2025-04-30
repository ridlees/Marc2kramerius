import requests as r
import json

def escape(uuid):
	return uuid.replace(':','\:').replace('-','\-')

PID = "uuid:022092ae-15d1-4c4e-a41c-f7e42248e864"
values = "datum_str", "details", "pid_path"
session = r.Session()
#response = session.get(f"https://kramerius.mzk.cz/search/"+ "api/v5.0/search?q=PID:" + escape(PID)+f"&fl=datum_str,details,pid_path&rows=1&start=0&wt=json", stream=True).json()
response = session.get("https://www.ndk.cz/search/" + "api/v5.0/search?q=PID:" + escape(PID)+f"&fl=datum_str,details,pid_path&rows=1&start=0&wt=json", stream=True).json()
docs = response.get("response").get("docs")
#print(docs)
page_URL_parts = docs[0].get("pid_path")[0].split("/")
page_url = f"https://ndk.cz/view/{page_URL_parts[-2]}?page={page_URL_parts[-1]}"
print(page_url)
page = docs[0].get("details")[0].split('\xa0\n')[0]
print(page)
date, month, year = docs[0].get("datum_str").split(".")
print(date, month, year)
#[{'datum_str': '21.8.1937', 'details': ['4\xa0\n                        ##NormalPage'], 'pid_path': ['uuid:bdc405b0-e5f9-11dc-bfb2-000d606f5dc6/uuid:2e856c90-2bf9-11dd-aaa1-000d606f5dc6/uuid:b818a150-3731-11dd-9a28-000d606f5dc6/uuid:022092ae-15d1-4c4e-a41c-f7e42248e864']}]

#https://ndk.cz/view/uuid:b818a150-3731-11dd-9a28-000d606f5dc6?page=uuid:022092ae-15d1-4c4e-a41c-f7e42248e864
