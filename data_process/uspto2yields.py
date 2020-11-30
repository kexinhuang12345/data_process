import csv, pickle 
from time import time 
import pandas as pd
t1 = time()
input_file = "raw_data/uspto_raw.txt"
output_file = "processed_data/uspto_yields.pkl"


with open(input_file, 'r') as fin:
	lines = fin.readlines()[1:]

'''
ReactionSmiles  PatentNumber    ParagraphNum    Year    TextMinedYield  CalculatedYield  

separated by \t 

can be empty 



[ClH:1].[OH:2][C:3]([C:34]1[CH:39]=[CH:38][CH:37]=[CH:36][CH:35]=1)([C:28]1[CH:33]=
[CH:32][CH:31]=[CH:30][CH:29]=1)[CH:4]1[CH2:9][CH2:8][N:7]([CH2:10][CH2:11][CH2:12]
[C:13]([C:15]2[CH:20]=[CH:19][C:18]([C:21]([CH3:27])([CH3:26])[C:22]([O:24][CH3:25])=[O:23])=
[CH:17][CH:16]=2)=[O:14])[CH2:6][CH2:5]1.[BH4-].[Na+].[OH-].[Na+].Cl>CO>[ClH:1].[OH:2][C:3]
([C:28]1[CH:33]=[CH:32][CH:31]=[CH:30][CH:29]=1)([C:34]1[CH:39]=[CH:38][CH:37]=[CH:36][CH:35]=1)
[CH:4]1[CH2:9][CH2:8][N:7]([CH2:10][CH2:11][CH2:12][CH:13]([C:15]2[CH:20]=[CH:19][C:18]([C:21]([CH3:27])
([CH3:26])[C:22]([O:24][CH3:25])=[O:23])=[CH:17][CH:16]=2)[OH:14])[CH2:6][CH2:5]1 |f:0.1,2.3,4.5,8.9|
'''


### filter out the line with empty yield 
valid_lines = list(filter(lambda line:len(line.split('\t')[4].strip())>0 , lines))
# valid_lines = valid_lines[:5000]
'''
1939254 lines in raw_file; 
857111  lines has CalculatedYield. 
859604  lines has TextMinedYield. 
'''

def line_to_tuple_len_4(line):
	reactions = line.split()[0]
	reactant, catalyst, product = reactions.split('>')
	yields = line.split('\t')[4]
	return [reactant, catalyst, product, yields]


valid_lines = list(map(line_to_tuple_len_4, valid_lines))


reaction_id_lst, reaction_dict_lst, yields_lst = [], [], []

with open(output_file, 'w') as csvfile:
	fieldnames = ["ID", "X", "Y"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	cnt = 1
	for i,line in enumerate(valid_lines):
		yields_str = line[3]
		'''
			outliers:
				xx to xx%
				> xx% 
				< xx% 
				>= xx%
				<= xx%
				~ xxx%

				weird symbol 
					'58 ± 2'
		'''
		if "to" in yields_str or ">" in yields_str or "<" in yields_str or "~" in yields_str:
			continue 
		try:
			yields = float(yields_str.strip()[:-1])/100
		except:
			# print(line)
			pass 


		reaction_id = "reactions_" + str(cnt)
		reaction_id_lst.append(reaction_id)
		cnt += 1
		reactions_dict = {"reactant": line[0], "catalyst": line[1], "product": line[2]}
		reaction_dict_lst.append(reactions_dict)
		yields_lst.append(yields)
		# writer.writerow({'ID': reaction_id, 'X': reactions_dict, 'Y': yields})


data = {"ID": reaction_id_lst, "X": reaction_dict_lst, "Y": yields_lst}
df = pd.DataFrame(data, columns = fieldnames)
pickle.dump(df, open(output_file, 'wb'))


# valid_reactions = []
# cnt = 1
# for line in valid_lines:
# 	yields_str = line[3]
# 	if "to" in yields_str or ">" in yields_str or "<" in yields_str or "~" in yields_str:
# 		continue 
# 	try:
# 		yields = float(yields_str.strip()[:-1])/100
# 	except:
# 		pass 

# 	reaction_id = "reactions_" + str(cnt)
# 	reactions_dict = {"reactant": line[0], "catalyst": line[1], "product": line[2]}
# 	cnt += 1
# 	# dic = {'ID': reaction_id, 'X':reactions_dict, 'Y': yields}
# 	lst = [reaction_id, reactions_dict, yields]
# 	valid_reactions.append(lst)

# pickle.dump(valid_reactions, open(output_file, 'wb'))


t2 = time()
print(int((t2-t1)/60), "minutes")







