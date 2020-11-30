input_file = "raw_data/drugbank.xml"
output_file = "processed_data/drugbank.csv"

import csv 
import xml.etree.ElementTree as ET




with open(output_file, 'w') as csvfile:
	fieldnames = ['ID1', 'X1', 'ID2', 'X2', 'Y', 'Map']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	# for i in range(3):
	# 	row_dict = {'ID1': reactant_id, 
	# 				'ID2': product_id, 
	# 				'X1': i[0], 
	# 				'X2': i[2], 
	# 				'Y': catalyst2idx[catalyst], 
	# 				'Map': catalyst}
	# 	writer.writerow(row_dict)



