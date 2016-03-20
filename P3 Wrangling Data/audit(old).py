import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import json

OSMFILE = "sacramento_california.osm"


#these regex queries will be used
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
skipped=["9311","9321"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# note that i'm putting only the lower variable mapping because in the update name i will use .lower
mapping = { "av":"Avenue",
            "ave": "Avenue",
            "ct": "Court",
            "crt": "Court",
            "hwy": "Highway",
            "pl": "Place",
            "st": "Street",
            "rd": "Road",
            "blvd":"Boulevard",
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
            "raod": "Road"
            }

postal_code_range = [94000,96000]

#creating the generator function; see Myles code
#https://discussions.udacity.com/t/parallelism-for-mapparser-py-or-how-to-make-your-code-run-faster/160952/6
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    Reference: http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_postal_code(invalid_postal_codes, postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
    except ValueError:
        invalid_postal_codes[postal_code] += 1

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    invalid_postal_codes = defaultdict(int)
    for i, elem in enumerate(get_element(osm_file)):
        for tag in elem.iter("tag"):
            if is_street_name(tag):
                audit_street_type(street_types, tag.attrib['v'])
            elif is_postal_code(tag):
                audit_postal_code(invalid_postal_codes, tag.attrib['v'])
    return [invalid_postal_codes, street_types]

audit_data = audit(OSMFILE)
#check the postal codes that don't fit in the range
pprint.pprint(audit_data[0])
#check the street types that don't fit with expected types
pprint.pprint(dict(audit_data[1]))



#Now, since we found the incorrect street types and postal codes, it is time
#to perform some corrections

def update_name(name, mapping):
    changed = []
    for part in name.split(" "):
        part = part.strip(",\.").lower()  
        if part in mapping.keys():
            part = mapping[part]
        changed.append(part.capitalize())
    return " ".join(changed)


def update_postal_code(postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
        else:
            return int(postal_code)
    except ValueError:
        return postal_code_default


#######See The Updated Values for street
for st_type, ways in audit_data[1].iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        # Show all street names in way nodes.
        print name, "=>", better_name


#######Define the shape of the model data
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
def shape_element(element):
    node = {}
    node['created'] = {}
    node['pos'] = [0,0]
    if element.tag == "way":
        node['node_refs'] = []
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        #attributes
        for k, v in element.attrib.iteritems():
            #latitude
            if k == 'lat':
                try:
                    lat = float(v)
                    node['pos'][0] = lat
                except ValueError:
                    pass
            #longitude
            elif k == 'lon':
                try:
                    lon = float(v)
                    node['pos'][1] = lon
                except ValueError:
                    pass
            #creation metadata
            elif k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
        #children
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']
            if problemchars.match(k): #ignore tags with problem characters
                continue
            if v in skipped: #ignore the weird address
                continue
            elif lower_colon.match(k): #split bases on colon
                k_split = k.split(':')
                #address fields
                if k_split[0] == 'addr':
                    k_item = k_split[1]
                    if 'address' not in node:
                        node['address'] = {}
                    #streets
                    if k_item == 'street':
                        v = update_name(v, street_mapping)                    
                    #postal codes
                    if k_item == 'postcode':
                        v = update_postal_code(v)
                    node['address'][k_item] = v
                    continue
        #way children
        if element.tag == "way":
            for n in element.iter('nd'):
                ref = n.attrib['ref']
                node['node_refs'].append(ref);
        return node
    else:
        return None



def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


process_map(OSMFILE, False)