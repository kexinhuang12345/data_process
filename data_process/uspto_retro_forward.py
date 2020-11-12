import csv 

input_file = "raw_data/uspto_raw.txt"
output_file = "processed_data/uspto_reaction.csv"


with open(input_file, 'r') as fin:
	lines = fin.readlines()[1:]

reactions = [line.split()[0] for line in lines]
reactions = [(reaction.split('>')[0],reaction.split('>')[2]) for reaction in reactions]

with open(output_file, 'w') as csvfile:
	fieldnames = ['reactant', 'product']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader() 
	for reactant, product in reactions: 
		writer.writerow({'reactants':reactant, 'product':product})	 

