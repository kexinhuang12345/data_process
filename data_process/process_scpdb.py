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

data_dir = "./new_datasets/scPDB"
files = os.listdir(data_dir)

ligand_pds, binding_site_pds = [], []
for file in files:
    binding_site = os.path.join(data_dir, f"{file}/site.mol2")
    ligand = os.path.join(data_dir, f"{file}/ligand.mol2")
    ligand_pd = PandasMol2().read_mol2(ligand)
    binding_site_pd = PandasMol2().read_mol2(binding_site)
    ligand_pds.append(ligand_pd.df)
    binding_site_pds.append(binding_site_pd.df)

dataset = {"pocket": binding_site_pds, "ligand": ligand_pds}
pickle.dump(dataset, open("processed_scpdb.pkl", 'wb'))