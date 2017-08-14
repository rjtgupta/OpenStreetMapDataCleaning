##Checking Street Names by analyzing the last value.
import xml.etree.ElementTree as ET
import re

OSM_FILE = "sample.osm"

file = open(OSM_FILE, "r")

accepted_names = ['Road','Way','Street','Avenue','Drive','Place','Boulevard',
                  'Court', 'South', 'North', 'Northwest', 'Northeast',
                  'Southwest', 'Southeast', 'East', 'West', 'Lane', 'Terrace',
                  'Circle', 'Ridge', 'Loop', 'Highway', 'Meridian', 'Parkway']

mapping = {'E':'East', 'W':'West', 'SW':'Southwest', 'NW':'Nothwest',
            'SE':'Southeast', 'NE':'Northeast', 'N':'North', 'S': 'South'}

Numbers_search = re.compile(r'[0123456789]')

def check_street(elem):
    '''
    Check the street name for abbreviations by analyzing the last word of the
    street name and correct it if necessary.
    '''
    vals = elem.attrib['v'].split()
    last = vals[len(vals)-1]
    if(last not in accepted_names):
        if((not Numbers_search.search(last))and (len(last) < 3)):
            if(last in mapping):
                street_name = ""
                for val in range (len(vals)-1):
                    street_name += vals[val]
                    street_name += " "
                street_name += mapping[last]
                print(street_name)
            else:
                print(elem.attrib['v'])
                
for event, elem in ET.iterparse(file):
    if(elem.tag == 'way'):
        for sub_elem in elem.iter('tag'):
            if(sub_elem.attrib['k']=='addr:street'):
                check_street(sub_elem)

'''
'check_street' makes the required changes to the street names and prints
out the correct names. A modified version of this function has been added to the
file "Cleaning.py".
'''
