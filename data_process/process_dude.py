# -*- coding: utf-8 -*-
# Author: TDC Team
# License: MIT
"""
This file contains a script to process the raw DUD-E data http://dude.docking.org/. 
"""

import os 
import pickle
import pandas as pd 
from biopandas.mol2 import PandasMol2
from biopandas.mol2 import split_multimol2
from biopandas.pdb import PandasPdb
from tqdm import tqdm

data_dir = "./new_datasets/dude"
files = os.listdir(data_dir)

ligand_pds, protein_pds = [], []
for file in tqdm(files):
    protein = os.path.join(data_dir, f"{file}/receptor.pdb")
    if not os.path.exists(os.path.join(data_dir, f"{file}/actives_final.mol2")):
        os.system(f'gzip -d {data_dir}/{file}/actives_final.mol2.gz')
    protein_pd = PandasPdb().read_pdb(protein)
    pdmol = PandasMol2()
    for mol2 in split_multimol2(os.path.join(data_dir, f"{file}/actives_final.mol2")):
        ligand_pd = pdmol.read_mol2_from_list(mol2_lines=mol2[1], mol2_code=mol2[0])
        ligand_pds.append(ligand_pd.df)
        protein_pds.append(protein_pd.df)

print (len(ligand_pds))
dataset = {"protein": protein_pds, "ligand": ligand_pds}
pickle.dump(dataset, open("processed_dude.pkl", 'wb'))