#Checking Counties in the Data Set within the source 'Tiger' to make sure all
#data is for the Seattle region only and is in the correct format.
import xml.etree.ElementTree as ET
import re

OSM_FILE = "sample.osm"

file = open(OSM_FILE, "r")

colon_search = re.compile(r'[:]')
semi_colon_search = re.compile(r'[;]')

def check_county (elem):
    if(colon_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(':')
        print("Before: " + elem.attrib['v'])
        print("After:  " + vals[0])
    elif(semi_colon_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(';')
        print("Before: " + elem.attrib['v'])
        print("After:  " + vals[0])
    
for event, elem in ET.iterparse(file):
    if(elem.tag == 'way'):
        for sub_elem in elem.iter('tag'):
            if(sub_elem.attrib['k']=='tiger:county'):
                check_county(sub_elem)


'''
The function "check_county" performs that funtion. A modified version of this
function has been added in the file "Cleaning.py".
'''
