#Checking the postal codes and making the required changes

import xml.etree.ElementTree as ET
import re

OSM_FILE = "sample.osm"

file = open(OSM_FILE, "r")

##Checking Postal Codes - if they have any 'funny' characters in them
Post_check = re.compile(r'[-/:,;#@!$%\ \t\r\n]')
hyphen_check = re.compile(r'[-]')
Alphabet_check = re.compile(r'([A-Z])')

def check_postalCodes(subelem):
    if((Alphabet_check.search(subelem.attrib['v']))):
        print(subelem.attrib['v'])
        return 0
    elif(hyphen_check.search(subelem.attrib['v'])):
        hyph_sep = subelem.attrib['v'].split('-')
        print(hyph_sep[0])
        return (hyph_sep[0])
    else:
        return (subelem.attrib['v'])
    

for event,elem in ET.iterparse(file):
    if(elem.tag=='way' or elem.tag=='node'):
        for subelem in elem.iter('tag'):
            if(subelem.attrib['k']=='addr:postcode'):
                check_postalCodes(subelem)
'''
Modified version of the function 'check_postalCodes' has been included in
'Cleaning.py'.
'''
