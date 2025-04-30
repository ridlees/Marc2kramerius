import requests as r
import json
from escape import escape


def getDocs(PID:str, URL:str) -> dict:
    session = r.Session()
    response = session.get(URL + "api/v5.0/search?q=PID:" + escape(PID)+"&fl=datum_str,details,pid_path,document_type&rows=1&start=0&wt=json", stream=True).json()
    return response.get("response").get("docs")

def getPublicationNumber(PID:str, URL:str, session:object) -> str:
    response = session.get(URL + "api/v5.0/search?q=PID:" + escape(PID)+"&fl=details&rows=1&start=0&wt=json", stream=True).json()
    publicationNumber = response.get("response").get("docs")[0].get("details")[0].split("##")[-1].replace("*","")
    return publicationNumber

def parseDoc(docs:dict, URL:str) -> tuple:
    page_URL_parts = docs[0].get("pid_path")[0].split("/")
    page_url = f"{URL}{page_URL_parts[-2]}?page={page_URL_parts[-1]}"
    page_number = docs[0].get("details")[0].split('\xa0\n')[0]
    publicationPID = page_URL_parts[-2]
    #page_number page_number.replace("[","").replace("]","")
    if page_number == "[1]":
            page_number = "1"
    #if the page is title page, MZK returns the data with in braces like this [1]
    date, month, year = docs[0].get("datum_str").split(".")
    return page_url, publicationPID, page_number, date, month, year



if __name__ == "__main__":
    session = r.Session()
    URL = "https://www.ndk.cz/search/"
    
    response = session.get(URL + "api/v5.0/search?q=PID:" + escape("uuid:a8a754b0-baf3-11dc-8c98-000d606f5dc6")+"&fl=details,pid_path&rows=1&start=0&wt=json", stream=True).json()
    print(response)
    docs = getDocs(response.get("response").get("docs")[0].get("pid_path")[0].split("/")[-2], URL)
    print(docs)
    print(parseDoc(docs, "https://www.ndk.cz/view/"))
    print(getDocs("uuid:10cf9a18-8671-4d75-9870-16308fb9f941", URL))
    #print(r.get("https://www.ndk.cz/search/api/v5.0/search?q=PID:"+ escape("uuid:b818a150-3731-11dd-9a28-000d606f5dc6") + "&fl=*&rows=1&start=0&wt=json").json())
    #print(getPublicationNumber("uuid:b818a150-3731-11dd-9a28-000d606f5dc6", "https://www.ndk.cz/search/", session))
    #print(getPublicationNumber("uuid:a0d97387-a89e-4942-b5bf-91ec9e366b39", "https://kramerius.mzk.cz/search/", session))
    #URL2 = "https://kramerius.mzk.cz/search/"
    #docs = getDocs("uuid:bdc405b0-e5f9-11dc-bfb2-000d606f5dc6", URL2)
    #print(docs)
    #print(parseDoc(docs, "https://www.digitalniknihovna.cz/mzk/view/"))

    """
    
    
    """
