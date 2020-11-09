import csv 
from collections import defaultdict
import rdkit
from rdkit import Chem, DataStructs

def remove_atom_num_in_smiles(smiles):
	mol = Chem.MolFromSmiles(smiles)
	mol = Chem.RemoveHs(mol)
	[a.ClearProp('molAtomMapNumber') for a in mol.GetAtoms()]
	smiles2 = Chem.MolToSmiles(mol)	
	return smiles2


'''
ReactionSmiles  PatentNumber    ParagraphNum    Year    TextMinedYield  CalculatedYield  
'''
input_file = "raw_data/uspto_raw_head50k.txt"
# input_file = "raw_data/uspto_raw.txt"
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

### filter out empty catalyst
valid_reactions = list(filter(lambda x:x[1] in most_common_catalyst, reactions))

products2idx = defaultdict(lambda:len(products2idx)+1)
reactants2idx = defaultdict(lambda:len(reactants2idx)+1)

with open(output_file, 'w') as csvfile:
	fieldnames = ['ID1', 'X1', 'ID2', 'X2', 'Y', 'Map']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for i in valid_reactions:
		try:
			product_cano_smiles = remove_atom_num_in_smiles(i[2])
		except:
			# print(i[2])
			continue 
		try:
			reactant_cano_smiles = remove_atom_num_in_smiles(i[0])
			reactant_cano_smiles_lst = reactant_cano_smiles.split('.')
			reactant_cano_smiles_lst.sort()
			reactant_cano_smiles = '.'.join(reactant_cano_smiles_lst)
		except:
			# print(i[0])
			continue 
		catalyst = i[1]

		product_id = "product_" + str(products2idx[product_cano_smiles])
		reactant_id = "reactant_" + str(reactants2idx[reactant_cano_smiles])

		row_dict = {'ID1': reactant_id, 
					'ID2': product_id, 
					'X1': i[0], 
					'X2': i[2], 
					'Y': catalyst2idx[catalyst], 
					'Map': catalyst}
		writer.writerow(row_dict)




## todo, looks many repetition. 



# print(len(products), len(reactants_lst), len(canonical_reactions))
# 20557 21184 26443


'''
smiles = 'C(C(CCCC)C[OH:5])C.C(N(CC)CC)C.[C:17]1([CH2:23][C:24](Cl)=[O:25])[CH:22]=[CH:21][CH:20]=[CH:19][CH:18]=1'
mol = Chem.MolFromSmiles(smiles)
mol = Chem.RemoveHs(mol)
[a.ClearProp('molAtomMapNumber') for a in mol.GetAtoms()]
smiles2 = Chem.MolToSmiles(mol)
print(smiles2)
'''









