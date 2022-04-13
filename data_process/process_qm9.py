## https://qmml.org/datasets.html download
## readme.txt 

import pandas as pd
import numpy as np
import os, sys, json, wget, subprocess
import torch, pickle 
# from torch_geometric.data import Data 
qm9_file = "dsgdb9nsd.xyz"

atom_types = ['C', 'N', 'O', 'H', 'F']
targets = ['A', 'B', 'C', 'mu', 'alpha', 'homo', 'lumo', 'gap', 'r2', 'zpve', 'U0', 'U', 'H', 'G', 'Cv', ]

'''
 1  tag       -            "gdb9"; string constant to ease extraction via grep
 2  index     -            Consecutive, 1-based integer identifier of molecule
 3  A         GHz          Rotational constant A
 4  B         GHz          Rotational constant B
 5  C         GHz          Rotational constant C
 6  mu        Debye        Dipole moment
 7  alpha     Bohr^3       Isotropic polarizability
 8  homo      Hartree      Energy of Highest occupied molecular orbital (HOMO)
 9  lumo      Hartree      Energy of Lowest occupied molecular orbital (LUMO)
10  gap       Hartree      Gap, difference between LUMO and HOMO
11  r2        Bohr^2       Electronic spatial extent
12  zpve      Hartree      Zero point vibrational energy
13  U0        Hartree      Internal energy at 0 K
14  U         Hartree      Internal energy at 298.15 K
15  H         Hartree      Enthalpy at 298.15 K
16  G         Hartree      Free energy at 298.15 K
17  Cv        cal/(mol K)  Heat capacity at 298.15 K
''' 

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
id_list = []
Y_list = []
while True:
	if lines[pointer][:4] == 'gdb ':
		properties = [float(i) for i in lines[pointer].strip().split()[2:]]
		properties = np.array(properties).reshape(1,-1)
		Y_list.append(properties)
		drug_id = '_'.join(lines[pointer].split()[:2])
		# assert len(properties) == 15
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
		data_list.append((atom_feature, positions))
		id_list.append(drug_id)

	pointer += 1
	if pointer == lines_num:
		break 

	if pointer % 2000 == 0:
		print(pointer)

	if pointer > 10000:
		break 

# pickle.dump(data_list, open('qm9.pkl', 'wb'))
# print(data_list[:3])
Y_list = np.concatenate(Y_list, 0)

df = pd.DataFrame()
df['X'] = pd.Series(data_list)
df['ID'] = pd.Series(id_list)
df = pd.concat([df, pd.DataFrame(Y_list, columns = targets)], axis = 1)
df.to_pickle('qm9.pkl')




