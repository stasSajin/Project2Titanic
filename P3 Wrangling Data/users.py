import xml.etree.ElementTree as ET
import pprint


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            users.add(element.get('uid'))
            element.clear()
    return users

users = process_map('sacramento_california.osm')
pprint.pprint(users)