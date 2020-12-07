from rdkit import Chem
from rdkit.Chem.PandasTools import LoadSDF
import csv 


file1 = "raw_data/qsar_200860192_sm_carcinogens.sdf"
file2 = "raw_data/qsar_200860192_sm_non-carcinogens.sdf"
output_file = "processed_data/carcinogens_lagunin.csv"

df = LoadSDF(file1, smilesName='SMILES')
pos_smiles = list(df['SMILES'])
label = [1] * len(pos_smiles)
df = LoadSDF(file2, smilesName = 'SMILES')
neg_smiles = list(df['SMILES'])
label.extend([0] * len(neg_smiles))
X = pos_smiles + neg_smiles 
IDs = ['Drug_'+str(i+1) for i in range(len(label))]
with open(output_file, 'w') as csvfile:
	fieldnames = ['ID', 'X', 'Y']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for x,y,iid in zip(X,label, IDs):
		writer.writerow({'ID':iid, 'X':x, 'Y':y})




# pos_mol = []
# neg_mol = []


# mols = Chem.SDMolSupplier(file1)
# for mol in mols:
# 	if mol is None:
# 		continue 
# 	try: 
# 		smiles = Chem.MolToSmiles(mol)
# 		pos_mol.append(smiles)
# 	except:
# 		pass


# mols = Chem.SDMolSupplier(file2)
# for mol in mols:
# 	if mol is None:
# 		continue 
# 	try:
# 		smiles = Chem.MolToSmiles(mol)
# 		neg_mol.append(smiles)
# 	except:
# 		pass 



# print(len(pos_mol + neg_mol))





'''

	Chem.MolToSmiles

'''
