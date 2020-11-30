import csv, os 

input_source_file_lst = ['raw_data/src-test.txt', 'raw_data/src-train.txt', 'raw_data/src-val.txt']
input_target_file_lst = [i.replace('src', 'tgt') for i in input_source_file_lst]
output_file = "processed_data/uspto50k.csv"

type_lst = []
product_lst = []
reactant_lst = []

def extract_type(line):
	string = line.split()[0].split('>')[0].split('_')[1]
	return int(string)

def extract_src_smiles(line):
	return ''.join(line.split()[1:])

def extract_tgt_smiles(line):
	return ''.join(line.strip().split())

for src, tgt in zip(input_source_file_lst, input_target_file_lst):
	with open(src, 'r') as fin:
		lines = fin.readlines()
	types = list(map(extract_type, lines))
	type_lst.extend(types)
	src_smiless = list(map(extract_src_smiles, lines))
	product_lst.extend(src_smiless)
	with open(tgt, 'r') as fin:
		lines = fin.readlines() 
	tgt_smiless = list(map(extract_tgt_smiles, lines))
	reactant_lst.extend(tgt_smiless)

with open(output_file, 'w') as csvfile:
	fieldnames = ['reactant', 'product', 'category']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader() 
	for reactant, product, category in zip(reactant_lst, product_lst, type_lst):
		dic = {'reactant': reactant, 'product': product, 'category': category}
		writer.writerow(dic)





