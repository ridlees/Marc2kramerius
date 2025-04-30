from pymarc import MARCReader
import re

def updateYear(year:str) -> int:
    yearWithCentury = int(year) + 1900
    if yearWithCentury > 1960:
        yearWithCentury = yearWithCentury - 100
    return yearWithCentury

def parseQ(q:str) -> tuple:
    splitQ = q.split(":") # if there is :, then there is the year
    # 4:236<4
    if len(splitQ) == 2: #The split happened and year is present
        rok = updateYear(splitQ[0]) #1904
        secondSplit = splitQ[1].split("<")
        print(secondSplit)
        if len(secondSplit) == 2:
            cislo = secondSplit[0]
            strana = secondSplit[1]
        else:
            cislo = secondSplit[0]
            strana = "NaN"
    else:
        thirdSplit = splitQ[0].split("<")
        if len(thirdSplit) == 2:
            rok = updateYear(thirdSplit[0])
            cislo = thirdSplit[1] # It returns values like 345, which is impossible to be page.
            strana = "NaN"
        
        else:
            rok = updateYear(splitQ[0])
            cislo = "NaN"
            strana = "NaN"
    print(rok, cislo, strana)
    if "/" in cislo:
        cislo = "NaN"
    return rok, cislo, strana
            
            
        
def readMarc(file:str) -> list:
    """ Main function that opens marcfile, reads the lines and add parsed records to records array
"""
    with open(file, 'rb') as f:
        with open("q.csv", "w") as output:
            output.write("101,Rok,Cislo,Strana\n")
            reader = MARCReader(f)
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
                    q = record.get('773').get('q')
                    if q == None:
                        continue
                    print(q)
                    rok, cislo, strana = parseQ(q)
                    output.write(f"{zerozeroone},{rok},{cislo},{strana}\n")
               
if __name__ == "__main__":
    readMarc("ucla_ret.mrc")
    
