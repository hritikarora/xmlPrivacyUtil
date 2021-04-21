import re
from bs4 import BeautifulSoup
import argparse
import fileinput
import random

parser = argparse.ArgumentParser() # for parsing command line argument list

parser.add_argument("-x",dest="xml",metavar="FILE1", required=True, help="xml input file")
parser.add_argument("-s",dest="spec",metavar="FILE2",required=True, help="Specification file")

args = parser.parse_args()

def maskOut(input):
    if input.name == "pincode":
        return "xxxxxx"
    elif input.name == "cvv":
        return "xxx"
    elif input.name == "cardnumber":
        return "xxxxxxxxxxxx"+input.text[:4]
    elif input.name == "ipaddress":
        return "127.1.1.1"
    elif input.name == "passportNumber":
        return "x"*len(input.text)
    elif input.name == "expiryDate":
        return "xx/xx"
    else :
        s = "x"*len(input.text)
        return s



maskElems = [] #elements that have to be masked
swapElems = [] #elements that have to be swapped
pseudoElems = [] #elements that have to be pseudonymized


# find all the elements that have to be filtered
htmlStream = ""

if args.spec:
    for line in fileinput.input(args.spec):
        htmlStream = htmlStream+line
    
    soup = BeautifulSoup(htmlStream, 'html.parser')

    elems = soup.find_all("datasource")
    for elem in elems:
        xp = elem.find("xpath")
        ftype = elem.find("filtertype")

        if ftype.text == "masking":
            maskElems.append(xp.text)
        elif ftype.text == "swapping":
            swapElems.append(xp.text)
        elif ftype.text == "pseudonymisation":
            pseudoElems.append(xp.text)

# apply techniques to the input file
if args.xml:

    with open(args.xml) as xml_file:
        xml_contents = xml_file.read()
        soup = BeautifulSoup(xml_contents, "xml")
    
    #masking
    for elem in maskElems:
        elems = soup.find_all(elem)
        for elem2 in elems:
            elem2['mask']=True
            elem2.string.replace_with(maskOut(elem2))
    print(soup)

    #swapping ex : ['firstname','lastname']
    # for i in range(0,len(swapElems)):
    #     elems = soup.find_all(swapElems[i])
    #     if len(elems)>1:




with open("final.xml", "w") as pascal_file:
    pascal_file.write(soup.prettify())