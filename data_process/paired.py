'''

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/drd2/train_pairs.txt

wget https://raw.githubusercontent.com/wengong-jin/iclr19-graph2graph/master/data/qed/train_pairs.txt



'''

import csv
import os.path as op

name_lst = ['drd2', 'qed', 'logp']

raw_data_folder = "./raw_data"
processed_data_folder = "./processed_data"


for name in name_lst:
	raw_file = op.join(raw_data_folder, name + "_pairs.txt")
	output_file = op.join(processed_data_folder, name + "_pairs.csv")
	with open(raw_file, 'r') as fin:
		lines = fin.readlines()
	with open(output_file, 'w') as csvfile:
		fieldnames = ['input', 'output']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for line in lines:
			input_smiles, output_smiles = line.strip().split()
			writer.writerow({'input': input_smiles, 'output':output_smiles})
	





