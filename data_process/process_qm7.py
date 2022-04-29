## https://qmml.org/datasets.html download
## readme.txt 

import pandas as pd
import numpy as np
import os, sys, json, wget, subprocess
import torch, pickle 
# from torch_geometric.data import Data 
qm7_file = "qm7/dsgdb7ae.xyz"
atom_types = ['C', 'N', 'O', 'H', 'S']

def atom2onehot(atom):
	onehot = np.zeros((1,len(atom_types)))
	idx = atom_types.index(atom)
	onehot[0,idx] = 1
	return onehot 

with open(qm7_file, 'r') as fin:
	lines = fin.readlines()

lines_num = len(lines)
pointer = 0


data_list = []
id_list = []
Y_list = []
while True:
	if int(lines[pointer]) == float(lines[pointer]) and '.' not in lines[pointer]:
		drug_id = 'Drug_' + lines[pointer].strip() 
		properties = float(lines[pointer+1])
		Y_list.append(properties)
		pointer += 2 
		atom_list = []
		position_list = []
		while True:
			line = lines[pointer]
			atom_vec = atom2onehot(line[0]) #### (1,5)
			position = np.array([float(i) for i in line.split()[1:4]]).reshape(1,3) ### (1,3)
			atom_list.append(atom_vec)
			position_list.append(position)
			pointer += 1
			if pointer >= lines_num or lines[pointer].strip() == '':
				break 
		atom_feature = np.concatenate(atom_list, 0)
		positions = np.concatenate(position_list, 0)
		# data = Data(x=atom_feature, pos=positions, y=properties)
		data_list.append((atom_feature, positions))
		id_list.append(drug_id)

	pointer += 1
	if pointer >= lines_num:
		break 

	if pointer % 2000 == 0:
		print(pointer)
	# if pointer > 10000:
	# 	break 

# pickle.dump(data_list, open('qm9.pkl', 'wb'))
print(data_list[:3])
Y_list = np.array(Y_list)

df = pd.DataFrame()
df['X'] = pd.Series(data_list)
df['ID'] = pd.Series(id_list)
df = pd.concat([df, pd.DataFrame(Y_list, columns = ['Y'])], axis = 1)
df.to_pickle('qm7.pkl')



