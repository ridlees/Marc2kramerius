import requests as r
import json
from escape import escape

def getRootPIDlist(ISSN:str, URL:str) -> list:
    # vrací ročník
    #root_pid
    URL = f"{URL}api/v5.0/search?q=issn:{ISSN}&fl=PID&rows=100000000&wt=json"     
    session = r.Session()
    response = session.get(URL, stream=True).json()
    docs = response.get("response").get("docs")
    return docs


if __name__ == "__main__":
    URL = "https://www.ndk.cz/search/"
    docs = getRootPIDlist("1802-6265", URL)
    print(docs)
    URL2 = "https://kramerius.mzk.cz/search/"
    getRootPIDlist("1802-6265", URL2)
