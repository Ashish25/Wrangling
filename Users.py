#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

# sorts a dictionary by its value
def sort_dictionary_by_count(dictionary, top = None):
    if top is None:
        top = len(dictionary)
        
    keys_dict = list(dictionary.keys())
    keys_dict.sort(key = lambda k : dictionary[k], reverse=True)
    count = 0

    for key in keys_dict:
        if top == count:
            break
        print("{}:{}".format(key, dictionary[key]))
        count += 1


# set of unique user_ids
def process_map(filename):
    users = set()
    for events, element in ET.iterparse(filename, events=('start', 'end')):
        if events == 'end':
            if 'uid' in element.attrib.keys():
            	if element.attrib['uid'] not in users:
            		users.add(element.attrib['uid'])
        		
    return users


# dict of unique users
def process_map_uid_and_name(filename):

    users = dict()

    for events, element in ET.iterparse(filename, events=('start', 'end')):
        if events == 'end':
            if 'uid' in element.attrib.keys():
                if element.attrib['uid'] not in users.keys():
                    users[element.attrib['uid']] = element.attrib['user']

    return users

# Entries per user
def process_map_user_variance(filename):

    num_entries = defaultdict(int)

    for events, element in ET.iterparse(filename, events=('start', 'end')):
        if events == 'end':
            if 'uid' in element.attrib.keys():
                num_entries[element.attrib['user']] += 1 

    return num_entries


def test():

    # users = process_map('kolkata_india.osm')
    # users = process_map_uid_and_name('kolkata_india.osm')
    num_entries = process_map_user_variance('kolkata_india.osm')
    sort_dictionary_by_count(num_entries, 30)
    # pprint.pprint(users)
    # print("\n", len(users))



if __name__ == "__main__":
    test()