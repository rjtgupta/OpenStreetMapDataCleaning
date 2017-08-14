from lxml import etree as ET
import re
import csv
import cerberus
import codecs
import pprint

#Import the Schema.
import Schema

#Input File
OSM_FILE = "seattle_washington.osm"

file = open(OSM_FILE, "r")

SCHEMA = Schema.doc_schema

#Target Files
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

#Table Column Names
nodes_table = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset',
               'timestamp']
nodes_tags_table = ['id', 'key', 'value', 'type']
ways_table = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
ways_tags_table = ['id', 'key', 'value', 'type']
ways_nodes = ['id', 'node_id', 'position']

#k attribute of 'tags' where correction has to be performed
value_correction = ['addr:postcode', 'tiger:county', 'source', 'addr:street']

#Different search commands to find various components in strings.
colon_search = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
semi_colon_search = re.compile(r'[;]')
c_search = re.compile(r'[:]')
space_search = re.compile(r' ')
alphabet_search = re.compile(r'([A-Z])')
hyphen_search = re.compile(r'[-]')
Numbers_search = re.compile(r'[0123456789]')
and_search = re.compile(r'[&]')
comma_search = re.compile(r'[,]')

def check_postalCodes(elem):
    '''
    Function to clean the 'postal codes'.
    If Alphabet present in postal code return 0 (postal code not in the U.S.).
    If hyphen present, keep the postal code (first part).
    If the above two are incorrect, the format is correct.
    '''
    sub_tag = {}
    key_type = elem.attrib['k'].split(':')
    sub_tag['type'] = key_type[0]
    sub_tag['key'] = key_type[1]
    if(alphabet_search.search(elem.attrib['v'])):
        return 0
    elif(hyphen_search.search(elem.attrib['v'])):
        hyph_sep = elem.attrib['v'].split('-')
        sub_tag['value']=hyph_sep[0]
    else:
        sub_tag['value'] = elem.attrib['v']

    return sub_tag

def check_street(elem):
    '''
    Check the street name for abbreviations by analyzing the last word of the
    street name and correct it if necessary.
    '''
    accepted_names = ['Road','Way','Street','Avenue','Drive','Place','Boulevard',
                  'Court', 'South', 'North', 'Northwest', 'Northeast', 'Broadway',
                  'Southwest', 'Southeast', 'East', 'West', 'Lane', 'Terrace',
                  'Circle', 'Ridge', 'Loop', 'Highway', 'Meridian', 'Parkway']

    mapping = {'E':'East', 'W':'West', 'SW':'Southwest', 'NW':'Nothwest',
            'SE':'Southeast', 'NE':'Northeast', 'N':'North', 'S': 'South'}

    sub_tag = {}
    key_type = elem.attrib['k'].split(':')
    sub_tag['type'] = key_type[0]
    sub_tag['key'] = key_type[1]
    
    vals = elem.attrib['v'].split()
    last = vals[len(vals)-1]
    if(last not in accepted_names):
        if((not Numbers_search.search(last))and (len(last)) < 3):
            if(last in mapping):
                street_name = ""
                for val in range (len(vals)-1):
                    street_name += vals[val]
                    street_name += " "
                street_name += mapping[last]
                sub_tag['value'] = street_name
                return sub_tag
        
    sub_tag['value'] = elem.attrib['v']
        
    return sub_tag

def check_source(elem):
    '''
    Clean the data source, by analyzing the different formats present in the
    XML file (sources present with and without ';','&',',') & standardize
    those values.
    '''
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
    respective values.
    '''
    bing_search = re.compile(r'bing', flags = re.IGNORECASE)
    yahoo_search = re.compile(r'yahoo', flags = re.IGNORECASE)
    knowledge_search = re.compile(r'knowledge', flags = re.IGNORECASE)
    tiger_search = re.compile(r'tiger', flags = re.IGNORECASE)
    pgs_search = re.compile(r'pgs', flags = re.IGNORECASE)
    usgs_search = re.compile(r'usgs', flags = re.IGNORECASE)
    mapquest_search = re.compile(r'mapquest', flags = re.IGNORECASE)
    
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
    
def check_county(elem):
    '''
    Clean the county names by searching for the presence of ':' or ';'. If
    present, return the sub_tag with the 'value' having the first part.
    '''
    sub_tag = {}
    key_type = elem.attrib['k'].split(':')
    sub_tag['type'] = key_type[0]
    sub_tag['key'] = key_type [1]
    
    if(colon_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(':')
        sub_tag['value'] = vals[0]
    elif(semi_colon_search.search(elem.attrib['v'])):
        vals = elem.attrib['v'].split(';')
        sub_tag['value'] = vals[0]
    else:
        sub_tag ['value'] = elem.attrib['v']

    return sub_tag

def add_tags(elem):
    '''
    Function to add the tags for both 'node' and 'way'. Call the required
    funtions to perform data cleaning.
    '''
    tags = []
    sub_tag = {}
    for sub_elem in elem.iter('tag'):
        #need to make sure that the attribute 'k' isn't specifying source. This
        #is because there may be multiple values which we may have to add for
        #this attribute. For the rest, need to add only one value per tag.
        sce = False
        if(sub_elem.attrib['k'] in value_correction):
            if(sub_elem.attrib['k']=="addr:postcode"):
                sub_tag = check_postalCodes(sub_elem)
                if(sub_tag==0):
                    break
                sub_tag['id'] = int(elem.attrib['id'])
            elif(sub_elem.attrib['k']=='addr:street'):
                sub_tag = check_street(sub_elem)
                sub_tag['id'] = int(elem.attrib['id'])
            elif(sub_elem.attrib['k']=='source'):
                sce = True
                sub_tag['id'] = int(elem.attrib['id'])
                sub_tag['type'] = 'regular'
                sub_tag['key'] = sub_elem.attrib['k']
                source_data = check_source(sub_elem)
                for source_val in source_data:
                    sub_tag['value'] = source_val
                    tags.append(sub_tag)
                    sub_tag = {}
                    sub_tag['id'] = int(elem.attrib['id'])
                    sub_tag['type'] = 'regular'
                    sub_tag['key'] = sub_elem.attrib['k']
            elif(sub_elem.attrib['k']=='tiger:county'):
                sub_tag = check_county(sub_elem)
                sub_tag['id'] = int(elem.attrib['id'])
        else:
            sub_tag['id'] = int(elem.attrib['id'])
            if(colon_search.search(sub_elem.attrib['k'])):
                vals = sub_elem.attrib['k'].split(':')
                if(len(vals)==2):
                    sub_tag['type'] = vals[0]
                    sub_tag['key'] = vals[1]
                else:
                    sub_tag['type'] = vals[0]
                    final_key = ""
                    for x in range (1, len(vals)):
                        final_key += vals[x]
                        final_key += ":"
                        final_key = final_key.strip(":")
                        sub_tag['key'] = final_key
                sub_tag['value'] = sub_elem.attrib['v']
            else:
                sub_tag['type'] = 'regular'
                sub_tag['key'] = sub_elem.attrib['k']
                sub_tag['value'] = sub_elem.attrib['v']
        if((sub_tag != 0) and (not sce)):
            tags.append(sub_tag)
            sub_tag = {}

    return tags

def add_values(elem):
    '''
    Function to store the data from the XML file into dictionaries and
    lists as required.
    '''
    way_vals  = {}
    way_nodes = []
    node_vals = {}
    tags = []
    
    if (elem.tag == 'way'):
        attributes_way = elem.attrib
        for att,val in attributes_way.items():
            if(att in ways_table):
                if((att == 'id') or (att == 'uid') or (att=='changeset')):
                    way_vals[att] = int(val)
                else:
                    way_vals[att] = val

        tags = add_tags(elem)

        count = 0
        sub_node = {}
        sub_node['id'] = way_vals['id']
        for sub_nodes in elem.iter('nd'):
            sub_node['node_id'] = int (sub_nodes.attrib['ref'])
            sub_node['position']= count
            count += 1
            way_nodes.append(sub_node)
            sub_node = {'id': way_vals['id']}

        return {'ways': way_vals, 'ways_nodes': way_nodes, 'ways_tags': tags}
            
    if (elem.tag == 'node'):
        attributes_node = elem.attrib
        for att,val in attributes_node.items():
            if(att in nodes_table):
                if((att == 'id')or(att == 'uid')or(att=='version')
                   or(att=='changeset')):
                    node_vals[att] = int(val)
                elif((att == 'lat')or (att == 'lon')):
                    node_vals[att] = float(val)
                else:
                    node_vals[att] = val
                
        tags = add_tags(elem)
        return {'nodes': node_vals, 'node_tags':tags}
                

def validate_element(element, validator, schema=SCHEMA):
    '''
    Make sure that the data structure adheres to the schema provided. Else,
    raise an Exception.
    '''
    if validator.validate(element, schema) is not True:
        print(element)
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

class UnicodeDictWriter(csv.DictWriter, object):
    '''
    Extend the class UnicodeDictWriter in order to write unicode values.
    '''
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def get_element(file_open, tags = ['way', 'node']):
    '''
    If the tag name is either 'way' or 'node', return that element.
    '''
    context =  ET.iterparse(file_open, events = ('start', 'end'))

    _, root = next(context)

    for event,elem in context:
        if(event=='end' and (elem.tag in tags)):
            yield elem
            while elem.getprevious() is not None:
                del elem.getparent()[0]


#Open the necessary files in binary mode for writing.
with codecs.open(NODES_PATH, 'wb') as nodes_file, \
    codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
    codecs.open(WAYS_PATH, 'wb') as ways_file, \
    codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
    codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:

    nodes_writer = UnicodeDictWriter(nodes_file, nodes_table)
    node_tags_writer = UnicodeDictWriter(nodes_tags_file, nodes_tags_table)
    ways_writer = UnicodeDictWriter(ways_file, ways_table)
    way_nodes_writer = UnicodeDictWriter(way_nodes_file, ways_nodes)
    way_tags_writer = UnicodeDictWriter(way_tags_file, ways_tags_table)

#Write the column names before inputing the data.
    nodes_writer.writeheader()
    node_tags_writer.writeheader()
    ways_writer.writeheader()
    way_nodes_writer.writeheader()
    way_tags_writer.writeheader()

#Initialize the schema validator
    validator = cerberus.Validator()

#Keep going through elements while there still are tags in the source file
    for _,elem in enumerate(get_element(file)):
        values = add_values(elem)
        
        validate_element(values, validator)

        if elem.tag == 'node':
            nodes_writer.writerow(values['nodes'])
            node_tags_writer.writerows(values['node_tags'])
        elif elem.tag == 'way':
            ways_writer.writerow(values['ways'])
            way_nodes_writer.writerows(values['ways_nodes'])
            way_tags_writer.writerows(values['ways_tags'])

        elem.clear()
