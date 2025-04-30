from pymarc import MARCReader
import re

class recordMarc:
    """ Class holding Marc record with fields for:
        001 (which holds the UUID for the record
        008 (which holds the year data, not used currently -> can be used if q field and g field are empty (which is not the case on this project)
        NK (holds the link to Národní knihovna)
        MZK (hold the link to Moravská zemská knihovna)
        rok (year of the publication)
        cislo (number of publication)
        strana (page, can be NaN, if so, we ignore it later
    """
    def __init__(self,zerozeroone:str):
        self.zerozeroone = zerozeroone

    def set008(self,set008:str):
        self.set008 = set008

    def setqField(self,rok:str,cislo:str,strana:str):
        self.rok = rok
        self.cislo = cislo
        self.strana = strana

def split_qField(qField:str)-> tuple:
    """function to split q field (ideally in format YY:PUBLICATION:PAGE) to get rok, cislo, strana
"""
    #if it has year
    if ":" in qField:
        first_split = qField.split(":")
        #if it has strana
        if "<" in first_split[1]:
            second_split = first_split[1].split("<")
            return first_split[0], second_split[0], second_split[1]
        #if it has cislo but no strana 
        return first_split[0], first_split[1], "NaN"

    # if it has no year
    if "<" in  qField:
        second_split = qField.split("<")
        return "NaN",second_split[0],second_split[1]
    return qField, "NaN", "NaN"

def g_unNan(recordMarc:recordMarc,record:MARCReader) -> None:
    """
function hat tries to fix NaN values in rok and cislo, however, currently there is no way to fix strana.

Note: připadně číst 773, G, kde je ročník nebo 008 kterej koduje na 8 poliček, první 4 kdy je první záznam a druhé 4 kdy vyšlo toto konkrétní periodikum. (12-15 je ročník), v 008 je to vždy.
    """
    if recordMarc.rok =="NaN":
        g = record.get('773').get('g')
        rok = g.split(",")[1][3:]
        recordMarc.rok = rok
    if recordMarc.cislo == "NaN":
        g = record.get('773').get('g')
        if re.match("^Roč\.\s\d{1,2},\s\d{4},\sč\.\s\d", g):
            cislo = g.split(",")[2].split(" ")[2]
            recordMarc.cislo = cislo
        else:
            recordMarc.set008(record.get('008'))
    if recordMarc.strana == "NaN":
        print("another one!")
        
def readMarc(file:str) -> list:
    """ Main function that opens marcfile, reads the lines and add parsed records to records array
"""
    with open(file, 'rb') as f:
        reader = MARCReader(f)
        records = []
        for record in reader:
            if record == None:
                continue
            sevenseventhree = record.get("773")
            if sevenseventhree == None:
                continue
            title = sevenseventhree.get("t")
            if title == None:
                continue
            if title == "Lidové noviny":
                zerozeroone = str(record["001"]).split("  ")[1]
                rec = recordMarc(zerozeroone)
                qField = record.get('773').get('q')
                if qField == None:
                    continue
                rok, cislo, strana = split_qField(qField)
                rec.setqField(rok, cislo, strana)
                g_unNan(rec,record)
                #print(f"For record {rec.zerozeroone}: \n This is record rok {rec.rok} \n This is record cislo {rec.cislo} \n This is record strana {rec.strana} \n")
                records.append(rec)
            
        print(len(records)) #6043
        return records        
if __name__ == "__main__":
    records = readMarc("ucla_ret.mrc")
    with open("records.csv", "w") as f:
        f.write("101,Rok,Cislo,Strana\n")
        for record in records:
            f.write(f"{record.zerozeroone},{record.rok},{record.cislo},{record.strana}\n")
            
