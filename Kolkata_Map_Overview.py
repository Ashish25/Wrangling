import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

# Sorts a dictionary by it value
def sort_dictionary_by_count(dictionary, top = None):
	if top is None:
		top = len(dictionary)

	keys_dict = list(dictionary.keys())
	keys_dict.sort(key = lambda k : dictionary[k], reverse=True)
	count = 0

	for key in keys_dict:
		if top == count:
			break
		print("{} => {}".format(key, dictionary[key]))
		count += 1


# Number of different tag elements
def tags_k_value(filename):
	tag_dict = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			tag_dict[element.attrib['k']] += 1

	return tag_dict

# Inconsistent PostalCodes
def postcode(filename):
	religion_names = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			if element.attrib['k'] == 'addr:postcode':
				religion_names[element.attrib['v']] += 1
			element.clear()
	return religion_names

# Diversity of Religion
def religion(filename):
	religion_names = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			if element.attrib['k'] == 'addr:postcode':
				religion_names[element.attrib['v']] += 1
			element.clear()
	return religion_names

# Popular Sports
def sport(filename):
	religion_names = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			if element.attrib['k'] == 'sport':
				religion_names[element.attrib['v']] += 1
			element.clear()
	return religion_names

# Popular shops
def shop(filename):
	religion_names = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			if element.attrib['k'] == 'shop':
				religion_names[element.attrib['v']] += 1
			element.clear()
	return religion_names

# Major source of data
def source(filename):
	religion_names = defaultdict(int)
	for events, element in ET.iterparse(filename, events = ('start','end')):
		if events == 'end' and element.tag == 'tag':
			if element.attrib['k'] == 'source':
				religion_names[element.attrib['v']] += 1
			element.clear()
	return religion_names


if __name__ == '__main__':

	d = tags_k_value('kolkata_india.osm')
	pprint.pprint(d)

	d = postcode('kolkata_india.osm')
	sort_dictionary_by_count(d)

	d = religion('kolkata_india.osm')
	sort_dictionary_by_count(d)

	d = sport('kolkata_india.osm')
	sort_dictionary_by_count(d)

	d = shop('kolkata_india.osm')
	sort_dictionary_by_count(d)

	d = source('kolkata_india.osm')
	sort_dictionary_by_count(d)	