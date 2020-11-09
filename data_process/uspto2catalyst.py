import csv 
from collections import defaultdict

'''
ReactionSmiles  PatentNumber    ParagraphNum    Year    TextMinedYield  CalculatedYield  
'''
input_file = "raw_data/uspto_raw_head50k.txt"
output_file = "processed_data/uspto_catalyst.csv"
most_common_k = 100 

with open(input_file, 'r') as fin:
	lines = fin.readlines()[1:]
reactions = [line.split()[0] for line in lines]
reactions = [line.split('>') for line in reactions]
reactions = list(filter(lambda reaction_tuple:len(reaction_tuple[1].strip()) > 0, reactions))




catalyst_lst = [i[1] for i in reactions]
catalyst2cnt = defaultdict(int)
for catalyst in catalyst_lst:
	catalyst2cnt[catalyst] += 1
catalyst2cnt = [(catalyst,cnt) for catalyst,cnt in catalyst2cnt.items()]
catalyst2cnt.sort(key = lambda x:x[1], reverse = True)
catalyst2cnt = catalyst2cnt[:most_common_k]
most_common_catalyst = [catalyst for catalyst,cnt in catalyst2cnt]
catalyst2idx = dict()
for i,catalyst in enumerate(most_common_catalyst):
	catalyst2idx[catalyst] = i+1 

valid_reactions = list(filter(lambda x:x[1] in most_common_catalyst, reactions))
products = [i[2] for i in valid_reactions]
reactants = [i[0] for i in valid_reactions]




with open(output_file, 'w') as csvfile:
	fieldnames = ['ID1', 'X1', 'ID2', 'X2', 'Y', 'Map']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	rowdict = {i:'' for i in fieldnames}
	writer.writerow(rowdict)











