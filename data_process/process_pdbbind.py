# -*- coding: utf-8 -*-
# Author: TDC Team
# License: MIT
"""
This file contains a script to process the raw scPDB data http://bioinfo-pharma.u-strasbg.fr/scPDB/. 
"""

import os 
import pickle
import pandas as pd 
from biopandas.mol2 import PandasMol2
from biopandas.pdb import PandasPdb
from tqdm import tqdm

data_dir = "./new_datasets/v2020-other-PL"
files = os.listdir(data_dir)

ligand_pds, binding_site_pds, protein_pds = [], [], []
for file in tqdm(files):
    if file == 'readme' or file == 'index':
        continue
    try:
        binding_site = os.path.join(data_dir, f"{file}/{file}_pocket.pdb")
        protein = os.path.join(data_dir, f"{file}/{file}_protein.pdb")
        ligand = os.path.join(data_dir, f"{file}/{file}_ligand.mol2")
        ligand_pd = PandasMol2().read_mol2(ligand)
        protein_pd = PandasPdb().read_pdb(protein)
        binding_site_pd = PandasPdb().read_pdb(binding_site)
        ligand_pds.append(ligand_pd.df)
        binding_site_pds.append(binding_site_pd.df)
        protein_pds.append(protein_pd.df)
    except:
        continue

dataset = {"pocket": binding_site_pds, "ligand": ligand_pds, "protein": protein_pds}
pickle.dump(dataset, open("processed_pdbbind.pkl", 'wb'))