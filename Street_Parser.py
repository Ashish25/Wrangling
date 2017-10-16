#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict

OSMFILE = "kolkata_india.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Road", "Avenue", "Park", "Sarani" , "Lane", "Block", "Connector", "Row", "Bagan", "Place"]


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):   
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))


if __name__ == '__main__':
    test()