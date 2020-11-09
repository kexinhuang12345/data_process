import csv 


input_file = "raw_data/uspto_raw_head5k.txt"
output_file = "processed_data/uspto_catalyst.csv"

with open(input_file, 'r') as fin:
	lines = fin.readlines()[1:]

'''
ReactionSmiles  PatentNumber    ParagraphNum    Year    TextMinedYield  CalculatedYield  
'''


def line_to_tuple_len_4(line):
	reactions = line.split()[0]
	reactant, catalyst, product = reactions.split('>')
	yields = line.split('\t')[4]
	return [reactant, catalyst, product, yields]


valid_lines = list(map(line_to_tuple_len_4, valid_lines))



with open(output_file, 'w') as csvfile:
	fieldnames = ["ID", "X", "Y"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i,line in enumerate(valid_lines):
		reaction_id = "reactions_" + str(i+1)
		reactions = '\t'.join(line[:3]) 
		yields = line[3]
		writer.writerow({'ID': reaction_id, 'X': reactions, 'Y': yields})











