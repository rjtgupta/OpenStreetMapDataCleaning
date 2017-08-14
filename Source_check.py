#Checking and standardizing the source values.
'''
As we saw in the file "Street_check_values", certain data has been repeated and
is not in the same format. Thus, standardization is performed here to make sure
that the data representing a source is consistent and if a tag has multiple
sources (separated by ',', ';', '&'), these values can be identified as seperate
and thus be added to the accordingly in "Cleaning.py".
'''
import xml.etree.ElementTree as ET
import re

OSM_FILE = "sample.osm"

file = open(OSM_FILE, "r")

#Checking for the presence of various characters and sub-strings in the source
#value
and_search = re.compile(r'[&]')
semi_colon_search = re.compile(r'[;]')
comma_search = re.compile(r'[,]')
bing_search = re.compile(r'bing', flags = re.IGNORECASE)
yahoo_search = re.compile(r'yahoo', flags = re.IGNORECASE)
knowledge_search = re.compile(r'knowledge', flags = re.IGNORECASE)
tiger_search = re.compile(r'tiger', flags = re.IGNORECASE)
pgs_search = re.compile(r'pgs', flags = re.IGNORECASE)
usgs_search = re.compile(r'usgs', flags = re.IGNORECASE)
mapquest_search = re.compile(r'mapquest', flags = re.IGNORECASE)
space_search = re.compile(r' ')

#Creating a list of standard values which will be mapped onto the current
#values at the required places.
accepted_values = ['Bing', 'Yahoo', 'NRCan-CanVec-10.0', 'data.seattle.gov',
                   'US-NPS_import_b2a6c900-5dcc-11de-8509-001e2a3ffcd7',
                   'Geobase_Import_2009','USGS', 'Knowledge', 'TIGER', 'PGS',
                   'tiger_import_20070610', 'GeoBase', 'GPS', 'survey',
                   'King County GIS', 'SDOT Bike Rack Import 2012',
                   'Garmin Forerunner 305', 'osmsync:dero', 'KCPV', 'GPX file',
                   'Pierce County', 'NRCan-CanVec-8.0', 'CanVec_Import_2009',
                   'City of Burien', 'MapQuest', 'Pierce County', 'wetap.org',
                   'Thurston Geodata', 'NOS ENC (US govt)', 'Neo Freerunner',
                   'http://www.wsdot.wa.gov/Projects/SR167/TacomaToEdgewood/designviz/i5interchange_viz.htm',
                   'http://www.fs.fed.us/r6/data-library/gis/olympic/hydronet_meta.htm'                
                   ]
def check_source(elem):
    '''
    Clean the data source, by analyzing the different formats present in the
    XML file (sources present with and without ';','&',',') & standardize
    those values.    
    '''
    final = []
    space_val_add = False

    if(and_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split('&')
        for i in range (len(vals)):
            vals[i] = vals[i].strip()
            vals[i] = conv_standard(vals[i])
            if(vals[i] in accepted_values):
                final.append(vals[i])
                space_val_add = True        
    elif(semi_colon_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(';')
        for i in range (len(vals)):
            vals[i] = conv_standard(vals[i])
            if(vals[i] in accepted_values):
                final.append(vals[i])
                space_val_add = True
    elif(comma_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(',')
        for i in range (len(vals)):
            vals[i] = vals[i].strip()
            vals[i] = conv_standard(vals[i])
            if(vals[i] in accepted_values):
                final.append(vals[i])
                space_val_add = True
    elif(space_search.search(elem.attrib['v'])):
        vals = conv_standard(elem.attrib['v'])
        if(vals in accepted_values):
            final.append(vals)
            space_val_add = True

    if(not space_val_add):
        vals = conv_standard(elem.attrib['v'])
        if(vals in accepted_values):
            final.append(vals)
        
    return final

def conv_standard(val):
    '''
    Search for the presence of certain words in strings and return the
    respective standard values.
    '''
    if(bing_search.search(val)):
        return "Bing"
    elif(yahoo_search.search(val)):
        return "Yahoo"
    elif(knowledge_search.search(val)):
        return "Knowledge"
    elif(tiger_search.search(val)):
        return "TIGER"
    elif(pgs_search.search(val)):
        return "PGS"
    elif(usgs_search.search(val)):
        return "USGS"
    elif(mapquest_search.search(val)):
        return "MapQuest"
    else:
        return val
    
data_source = {}
for event, elem in ET.iterparse(file):
    if((elem.tag=='way')or (elem.tag == 'node')):
        for sub_elem in elem.iter('tag'):
            if (sub_elem.attrib['k']=='source'):
                values = check_source(sub_elem)
                for vals in values:
                    if(vals not in data_source):
                        data_source[vals] = 1
                    else:
                        data_source[vals] += 1
                
for i,j in data_source.items():
    print (i + " : " + str(j))
'''
Modified version of the function 'check_source' has been included in the
'Cleaning.py' file. The function 'conv_standard' is added as is.
'''
