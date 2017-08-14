#Printing out the existing values of the tag with attribute k titled 'source'
#for further analysis
import xml.etree.ElementTree as ET

OSM_FILE = "sample.osm"

file = open(OSM_FILE, "r")

data_source = {}
for event, elem in ET.iterparse(file):
    if((elem.tag=='way')or (elem.tag == 'node')):
        for sub_elem in elem.iter('tag'):
            if (sub_elem.attrib['k']=='source'):
                if(sub_elem.attrib['v'] not in data_source):
                    data_source[sub_elem.attrib['v']] = 1
                else:
                    data_source[sub_elem.attrib['v']] += 1

for i,j in data_source.items():
    print (i + " : " + str(j))
               
'''
Further cleaning is performed in the file 'Source_check.py'
'''
