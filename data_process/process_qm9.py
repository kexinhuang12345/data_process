## https://qmml.org/datasets.html download
## readme.txt 

import torch, pickle 
# from torch_geometric.data import Data 
qm9_file = "dsgdb9nsd.xyz"

import numpy as np 

atom_types = ['C', 'N', 'O', 'H', 'F']

def atom2onehot(atom):
	onehot = torch.zeros(1,len(atom_types))
	idx = atom_types.index(atom)
	onehot[0,idx] = 1
	return onehot 

with open(qm9_file, 'r') as fin:
	lines = fin.readlines()

lines_num = len(lines)
pointer = 0


data_list = []
while True:
	if lines[pointer][:4] == 'gdb ':
		properties = torch.FloatTensor([float(i) for i in lines[pointer].strip().split()[2:]])
		assert len(properties) == 15
		pointer += 1 
		atom_list = []
		position_list = []
		while lines[pointer][0] in atom_types:
			line = lines[pointer]
			atom_vec = atom2onehot(line[0]) #### (1,5)
			position = torch.FloatTensor([float(i) for i in line.split()[1:4]]).view(1,3) ### (1,3)
			atom_list.append(atom_vec)
			position_list.append(position)
			pointer += 1
		atom_feature = torch.cat(atom_list, 0)
		positions = torch.cat(position_list, 0)
		# data = Data(x=atom_feature, pos=positions, y=properties)
		data_list.append((atom_feature, positions, properties))
		# data_list.append(data)

	pointer += 1
	if pointer == lines_num:
		break 

	if pointer % 2000 == 0:
		print(pointer)

pickle.dump(data_list, open('qm9.pkl', 'wb'))
print(data_list[:3])






