## https://moleculenet.org/datasets-1  
## https://qmml.org/datasets.html download

import pandas as pd
import numpy as np
qm8_file = "qm8/qm8.sdf"
from rdkit.Chem.PandasTools import LoadSDF 
df = LoadSDF(qm8_file, smilesName='SMILES', removeHs=False)


'''
>>> df.columns
>>>	['ID', 'SMILES', 'ROMol']  '''
mol_lst = df['ROMol'].tolist() 
raw_id_lst = df['ID'].tolist() 
feature_lst = []
id_list = []
Y_list = []
for i,mol in enumerate(mol_lst):
	id_list.append(raw_id_lst[i].split('\t')[0])
	y = np.array([float(i) for i in raw_id_lst[i].strip().split('\t')[1:]]).reshape(1,-1)
	Y_list.append(y)
	atom_lst = []
	position_lst = []
	conformer = mol.GetConformer(id=0)
	for i in range(mol.GetNumAtoms()):
		atom = mol.GetAtomWithIdx(i).GetSymbol() 
		atom_lst.append(atom)
		position = conformer.GetAtomPosition(i)
		position = np.array([position.x, position.y, position.z]).reshape(1,-1) 
		position_lst.append(position)
	position = np.concatenate(position_lst)
	feature_lst.append((atom_lst, position))

print(feature_lst[:3])
Y_list = np.concatenate(Y_list, 0)
labels_name = ['E1-CC2', 'E2-CC2', 'f1-CC2', 'f2-CC2', 'E1-PBE0', 'E2-PBE0', 'f1-PBE0', 'f2-PBE0', 'E1-PBE0', 'E2-PBE0', 'f1-PBE0', 'f2-PBE0', 'E1-CAM', 'E2-CAM', 'f1-CAM',]

print("number of data points", Y_list.shape[0])

df = pd.DataFrame()
df['X'] = pd.Series(feature_lst)
df['ID'] = pd.Series(id_list)
df = pd.concat([df, pd.DataFrame(Y_list, columns = labels_name)], axis = 1)
df.to_pickle('qm8/qm8.pkl')


