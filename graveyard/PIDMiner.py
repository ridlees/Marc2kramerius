from listrootPIDs import getRootPIDlist
from listPublications import getPublication
import json

#FROM ISSN TO PAGE PID

if __name__ == "__main__":
    URL = "https://www.ndk.cz/search/"
    docs = getRootPIDlist("1802-6265", URL)
    print(len(docs))
    data = []
    for PID in docs:
        data = data + getPublication(PID.get("PID"), URL)
    print(data)
    with open("silenství.json", "w") as outfile:
        json.dump(data, outfile)


    URL2 = "https://kramerius.mzk.cz/search/"
    docs = getRootPIDlist("1802-6265", URL2)
    print(len(docs))
