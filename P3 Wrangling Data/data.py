import xml.etree.ElementTree as ET
import re
import codecs
import json
import os

"""
You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.
"""

'''
I found this discussion very helpful when creasting this code and wiriting up the update_name and update_postal code within
the shape_element function:
https://discussions.udacity.com/t/tag-types-and-improving-street-names-locally/46437/28
'''
#Search for problem characters
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
#Search for cases that have double colons in them
double_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
#search for street type ending (e.g., dr.)
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) 
#search if there is a colon in name
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#skip,changes, and mapping retrieved from looking at the results of audit.py
'''
Basically, I'm removing several street names that don't correspond
to an actual street name or are not part of sac area
'''
deleted=["9311","9321","PO Box 5259","11th Street, Fifth Floor", 'Industrial',
      'Fair Oaks Boulevard, Fair Oaks, CA 95628-7416',
      'Ne Side Next To Aquatic Center']


#next, I provide a dictionary of street names that were incorrectly specified
correctedStreets = { 'Promenade Circle #110': 'Promenade Circle',
           'Sw Cnr Sierra College Blvd / Sr 193': 'Southwest Center Sierra College Boulevard',} 




#next, I'm correcting the street name abbreviations
mapping = { "av":"Avenue",
            "ave": "Avenue",
            "ct": "Court",
            "crt": "Court",
            "hwy": "Highway",
            "pl": "Place",
            "st": "Street",
            "rd": "Road",
            "blvd":"Boulevard",
            "boulevar":"Boulevard",
            "dr": "Drive",
            "sq": "Square",
            "ln": "Lane",
            "trl": "Trail",
            "pkwy": "Parkway",
            "ne": "Northeast",
            "se": "Southeast",
            "nw": "Northwest",
            "sw": "Southwest",
            "crn":"Corner",
            "cnr":"Corner",
            "int":"Intersection",
            "@" : "At",
            "pt": "Point",
            "placez" : "Plaza",
            "raod": "Road",
            "road)":"Road"
            }


def update_name(name, mapping):
    changed = []
    for part in name.split(" "):
        part = part.strip(",\.").lower()  
        if part in mapping.keys():
            part = mapping[part]
        changed.append(part.capitalize())
    return " ".join(changed)

file_in = 'sacramento_california.osm' 

#I used the code to check for postal codes here
#the postal code ranges from 94000 to 96000. There is one postal code 96816
#that corresponds to honollulu, hawai. The code was inserted incorrectly
postal_code_range = [94000,96000]
def update_postal_code(postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
        else:
            return int(postal_code)
    except:
        return None

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
def shape_element(element):
    """
    create a dictionary for output node element. specify two values for the dictionary
    where one value stores the metadata and the other stores pos
    """
    node = {}
    node['created'] = {}
    node['pos'] = [0,0]
    if element.tag == "node" or element.tag == "way":
        #input the first level tags
        node['type'] = element.tag
        for k, v in element.attrib.items(): #iterate through each 1st level attributes of tag 'node' or 'way'
            #latitude extraction
            if k == 'lat':
                try:
                    lat = float(v)
                    node['pos'][0] = lat
                except ValueError:
                    pass
            #longitude extraction
            elif k == 'lon':
                try:
                    lon = float(v)
                    node['pos'][1] = lon
                except ValueError:
                    pass
            #extraction of metadata
            elif k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
            #avoid importing any blank keys or values
            if k == "" or v == "": 
                continue
            if k == 'id': #id is a first level attribute
                node['_id'] = v 
                continue
            node[k] = v
        #children
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']
            #if tag has problem character, then continue
            if re.search(problemchars, k):
                continue
            #if tag has one of the wrong street addresses, continue
            if k in deleted:
                continue
            #if tag is in one of the correctedStreets dictionary, change it
            if k in correctedStreets:
                k=correctedStreets[k]
            elif k.startswith("addr:"): #split bases on colon
                k_split = k.split(':')
                #address fields
                if k_split[0] == 'addr':
                    k_item = k_split[1]
                    if 'address' not in node:
                        node['address'] = {}
                    #update the streets with correct mappings
                    if k_item == 'street':
                        v = update_name(v, mapping)                    
                    #update postal code
                    if k_item == 'postcode':
                        v = update_postal_code(v)
                    node['address'][k_item] = v
                    continue
            elif lower_colon.match(k):
                node[k] = v
            else:
                node[k] = v
    #way children
        nd_ref=[]
        for child in element.iter("nd"):
            nd_ref.append(child.attrib['ref'])
        # If the resulting list isn't empty,
        if nd_ref != []:
            # Add the list under the node 'node_refs'
            node['node_refs'] = nd_ref
        return node
    else:
        #if the element doesn't belong to node or way
        return None

def process_map(file_in, pretty = False):    
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    counter = 0 #added counter to show status when creating json file
    with codecs.open(file_out, "w") as fo:        
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            counter += 1
            print counter
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
      
data = process_map(file_in, False)