import requests as r
import json
from escape import escape
import time

class pageItem:
    
    def __init__(self,rok:str,cislo:str,strana:str, URL:str):
        self.rok = rok
        self.cislo = cislo
        self.strana = strana
        self.URL = URL

ISSN = "1802-6265"
URLNDK = "https://www.ndk.cz/"
URLMZK = "https://kramerius.mzk.cz/search/"
requestBatchSize = 1000

def getRootPID(ISSN:str, URL:str) -> list:
    # returns just root_pid
    URL = f"{URL}search/api/v5.0/search?q=issn:{ISSN}&fl=root_pid&rows=1&wt=json"     
    session = r.Session()
    response = session.get(URL, stream=True).json()
    rootPid = response.get("response").get("docs")[0].get("root_pid")
    return rootPid

def getPages(root_pid:str, URL:str) -> list:
    session = r.Session()
    data = []
    response = session.get(URL + "search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:page&fl=PID&rows=1&start=999999&wt=json", stream=True)
    numFound = response.json().get("response").get("numFound")
    print(numFound) #s238725
    batchSize = int(numFound/requestBatchSize + 1) #24
    for i in range(0,batchSize):
        slicer = i*requestBatchSize
        time.sleep(1) # The server keeps getting overwhelmed, so I am introducing sleep to ease the requests
        response = session.get(URL + "search/api/v5.0/search?q=root_pid:" + escape(root_pid)+f" AND document_type:page&fl=datum_str,details,pid_path&rows={batchSize}&start={slicer}&wt=json", stream=True)
        response.raise_for_status()
        response = response.json()
        data.append(response)
    return data

def getCislo(PID:str, URL:str) -> str:
    try:
        session = r.Session()
        response = session.get(URL + "search/api/v5.0/search?q=PID:" + escape(PID)+"&fl=details&rows=1&start=0&wt=json", stream=True).json()
        publicationNumber = response.get("response").get("docs")[0].get("details")[0]
        publicationNumber = publicationNumber.split("##")[-1].replace("*","")
        return publicationNumber
    except:
        session = r.Session()
        response = session.get(URL + "search/api/v5.0/search?q=PID:" + escape(PID)+"&fl=details,pid_path&rows=1&start=0&wt=json", stream=True).json()
        cislo = response.get("response").get("docs")[0].get("pid_path")[0].split("/")[-2]
        response = session.get(URL + "search/api/v5.0/search?q=PID:" + escape(cislo)+"&fl=details,pid_path&rows=1&start=0&wt=json", stream=True).json()
        publicationNumber = response.get("response").get("docs")[0].get("details")[0]
        publicationNumber = publicationNumber.split("##")[-1].replace("*","")
        return publicationNumber

def getPublications(root_pid:str, URL:str) -> dict:
    session = r.Session()
    data = []
    listCisel = {}
    response = session.get(URL + "search/api/v5.0/search?q=root_pid:" + escape(root_pid)+" AND document_type:periodicalitem&fl=PID&rows=1&start=999999&wt=json", stream=True)
    numFound = response.json().get("response").get("numFound")
    print(numFound) #29412
    batchSize = int(numFound/requestBatchSize + 1) #24
    for i in range(0,batchSize):
        slicer = i*requestBatchSize
        time.sleep(1) # The server keeps getting overwhelmed, so I am introducing sleep to ease the requests
        response = session.get(URL + "search/api/v5.0/search?q=root_pid:" + escape(root_pid)+f" AND document_type:periodicalitem&fl=details,pid_path&rows={batchSize}&start={slicer}&wt=json", stream=True)
        response.raise_for_status()
        response = response.json()
        data.append(response)
    for dataResponse in data:
        responseLine = dataResponse.get("response").get("docs")
        for line in responseLine:
            publicationNumber = line.get("details")[0]
            publicationNumber = publicationNumber.split("##")[-1].strip().replace("*","")
            pid = line.get("pid_path")[0].split("/")[-1]
            if not pid in listCisel:
                listCisel[pid] = publicationNumber
            
    return listCisel
    

def parseListPIDs(data:list, URL:str, name:str, listCisel:dict = {}) -> list:
    with open(f"{name}.csv", "w") as outfile:
        outfile.write("Rok,Cislo,Strana,URL\n")
        for response in data:
            responseLine = response.get("response").get("docs")
            for line in responseLine:
                time.sleep(1)
                try:
                    datum = line.get("datum_str").split(".")[2]
                except:
                    datum = line.get("datum_str")
                cislo = line.get("pid_path")[0]
                page_URL_parts = cislo.split("/")
                page_url = f"{URL}view/{page_URL_parts[-2]}?page={page_URL_parts[-1]}"
                #print(page_URL_parts[-2])
                if page_URL_parts[-2] in listCisel:
                    cislo = listCisel[page_URL_parts[-2]].replace("a","")
                else:
                    listCisel[page_URL_parts[-2]] = getCislo(page_URL_parts[-2], URL)
                    cislo = listCisel[page_URL_parts[-2]].replace("a","")
                try:
                    strana = line.get("details")[0].split('\xa0\n')[0]
                    strana = strana.strip().replace("[","").replace("]","").replace("(","").replace(")","").replace("a","").replace("b","").replace("c","").replace("d","").split(" ")[0]
                except:
                    strana = "X"
                item = pageItem(datum, cislo, strana,page_url)
                outfile.write(f"{item.rok},{item.cislo},{item.strana},{item.URL}\n")

if __name__ == "__main__":
    rootPid = getRootPID(ISSN, URLNDK)
    data = getPages(rootPid, URLNDK)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    listCisel = getPublications(rootPid, URLNDK)
    print(listCisel)
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(listCisel, f, ensure_ascii=False, indent=4)
    parseListPIDs(data, URLNDK, "NDK", listCisel)
    
        
