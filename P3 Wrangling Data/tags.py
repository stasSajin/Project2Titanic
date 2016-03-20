import xml.etree.ElementTree as ET
import pprint
import re
import os

#the regular expression we are checking for
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if re.search(lower, element.attrib['k']):        
            keys['lower'] += 1            
        elif re.search(lower_colon, element.attrib['k']):
            keys['lower_colon'] += 1            
        elif re.search(problemchars, element.attrib['k']):
            keys['problemchars'] += 1
            print element            
            print element.attrib['k']            
        else:
            keys['other'] += 1                 
    
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        element.clear()
    return keys

keys = process_map('sacramento_california.osm')
pprint.pprint(keys)