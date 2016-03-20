import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import os



def count_tags(filename):
    counts = defaultdict(int)
    for event, node in ET.iterparse(filename):
        if event == 'end': 
            counts[node.tag]+=1
        node.clear()             
    return counts


counts = count_tags('sacramento_california.osm')
pprint.pprint(counts)