import csv 

'''
ReactionSmiles  PatentNumber    ParagraphNum    Year    TextMinedYield  CalculatedYield  
'''
input_file = "raw_data/uspto_raw_head5k.txt"
output_file = "processed_data/uspto_catalyst.csv"

with open(input_file, 'r') as fin:
	lines = fin.readlines()[1:]
reactions = [line.split()[0] for line in lines]
reactions = [line.split('>') for line in reactions]
reactions = list(filter(lambda reaction_tuple:len(reaction_tuple[1].strip()) > 0, reactions))





# with open(output_file, 'w') as csvfile:
# 	fieldnames = ['ID1', 'X1', 'ID2', 'X2', 'Y', 'Map']
# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 	writer.writeheader()

# 	rowdict = {i:'' for i in fieldnames}
# 	writer.writerow(rowdict)











