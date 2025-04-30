import requests as r
import json
from escape import escape
from listrootPIDs import getRootPIDlist


#vrací publikace

def getPublication(PID:str) -> list:
    session = r.Session()
    data = []
    for i in range(0,15):
        slicer = i*27500
        response = session.get(f"https://www.ndk.cz/search/" + "api/v5.0/search?q=PID:" + escape(PID)+f"&fl=*&rows=27500&start={slicer}&wt=json", stream=True)
        response.raise_for_status()
        response = response.json()
        data.append(response)
    return data
if __name__ == "__main__":
    URL = "https://www.ndk.cz/search/"
    data = getPublication("uuid:5d8da3a0-546f-11ed-8291-5ef3fc9bb22f")
    with open("NDK.json", "w") as outfile:
        json.dump(data, outfile)
    URL2 = "https://kramerius.mzk.cz/search/"
    data = getPublication("uuid:7f141240-6ef8-11ed-87ef-005056825209")
    with open("MZK.json", "w") as outfile:
        json.dump(data, outfile)
