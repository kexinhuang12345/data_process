'''

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/drd2/train_pairs.txt

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/qed/train_pairs.txt



'''

import csv
import os.path as op


raw_data = "./raw_data/moses.csv"
processed_data = "./processed_data/moses.csv"


with open(raw_data, 'r') as csvfile:
	rows = list(csv.reader(csvfile, delimiter = ','))[1:]
	smiles_lst = []
	for row in rows:
		smiles_lst.append(row[0])

with open(processed_data, 'w') as csvfile:
	fieldnames = ['smiles']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader() 
	for smiles in smiles_lst:
		writer.writerow({'smiles':smiles})







