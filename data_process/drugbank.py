input_file = "raw_data/drugbank.xml"
output_file = "processed_data/drugbank.csv"

import csv 
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse
from collections import defaultdict

'''


<drugbank-id>DB04299</drugbank-id>

<name>Lepirudin</name>

<mechanism-of-action>xxxxxxxxx.</mechanism-of-action>


<indication>xxxxxxx.</indication>


<kind>SMILES</kind>

'''




# https://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p04_parse_huge_xml_files_incrementally.html 
def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass



doc = iterparse(input_file, ('start', 'end'))
# event, elem = next(doc)
# print(event, elem)
# event, elem = next(doc)
# print(event, elem)
# Skip the root element
stack = []

def normalize_tag(tag):
	return tag.split('}')[-1]

with open(output_file, 'w') as csvfile:
	fieldnames = ['DrugBank_ID', 'SMILES', 'Description', 'Indication', 'Mechanism of Action']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	in_drug = False 

	row_dict = defaultdict(str)
	for event, elem in doc:
		print(stack[1:])

		if event == 'start':				
			stack.append((normalize_tag(elem.tag), elem.text.strip() if elem.text is not None else ''))

		elif event == 'end':
			assert normalize_tag(elem.tag) == stack.pop()[0]

		print(event + ':', "\t\ttag>>>", elem.tag.split('}')[-1] + ';\t', "contents>>>", elem.text, '\n')


# tree = ET.parse(input_file)
# root = tree.getroot() 




# # write output file 



# 	# writer.writerow(row_dict)



