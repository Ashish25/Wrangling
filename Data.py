#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

# Regular Expressions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Expected Street Names
expected = ["Street", "Road", "Avenue", "Park", "Sarani" , "Lane", "Block", "Connector", "Row", "Bagan", "Place"]

# User details
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#Location of the Node
LOCATION = ['lat','lon']

#Checks to see if the tag is a Street name 
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


mapping = { "St": "Street",
            "Rd" : "Road",
            "Raod": "Road",
            "Ln": "Lane"
            }


# Updates the Street Names based on the above listed mapping
def update_name(name, mapping):
    match = street_type_re.search(name)
    match = match.group(0)
    if match in mapping.keys():
        name = name.replace(match,mapping[match])
        
    return name



#Cleans the Street names , making them Uniform
def clean_street_name(street_name):
    street_name = street_name.title()
    street_name = street_name.split(",")[0]
    street_name = street_name.split("(")[0]
    street_name = street_name.strip()
    street_name = update_name(street_name, mapping)

    return street_name


def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def clean_postal_code(postcode):
    return postcode.replace(" ","")


#Converts the Nodes into proper shaped Dictionaries
def shape_element(element):
    node = {}
    node['created'] = dict()

    #Checks for only nodes and ways
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        attributes = element.attrib

        for key, value in attributes.items():
            if key in CREATED:
                node['created'][key] = value
            elif key in LOCATION:
                node.setdefault('pos',[]).insert(0,float(value))
            else:
                node[key] = value

        for child in element:
                #children are of type nd
            if child.tag == 'nd':
                node.setdefault('node_refs',[]).append(child.attrib['ref'])
            elif child.tag == 'tag':
                #children are of type tag
                k = child.attrib['k']
                v = child.attrib['v']

                #If the tags are of type street name , then clean it
                if is_street_name(child):
                    v = clean_street_name(v)

                if is_postal_code(child):
                    v = clean_postal_code(v)
                    if len(v) > 6:
                        continue

                if problemchars.search(k) or k.count(":") > 1:
                    pass
                elif k.startswith('addr:'):
                    node.setdefault('address',{})[ k.split(":")[1] ] = v
                else:
                    node[k] = v
        return node
    else:
        return None

#Processes the Nodes, converts them into proper dictionary format and stores them in JSON format
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


if __name__ == "__main__":
    print("\n")
    data = process_map('kolkata_india.osm', True)
    pprint.pprint(data[0])
    print("\n")