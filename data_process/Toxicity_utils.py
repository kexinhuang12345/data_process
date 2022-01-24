import pandas as pd
import numpy as np
import os, sys, json, wget, subprocess
import warnings
warnings.filterwarnings("ignore")

from .. import utils

def Tox21_process(name, path, target = None):

	utils.download_unzip(name, path, 'tox21.csv')

	df = pd.read_csv(os.path.join(path,'tox21.csv'))
	
	df = df[df[target].notnull()].reset_index(drop = True)
	df = df.iloc[df['smiles'].drop_duplicates(keep = False).index.values]

	y = df[target].values
	drugs = df.smiles.values
	drugs_idx = df["mol_id"].values

	return drugs, y, drugs_idx

def ToxCast_process(name, path, target = None):

	utils.download_unzip(name, path, 'toxcast_data.csv')

	df = pd.read_csv(os.path.join(path,'toxcast_data.csv'))
	
	df = df[df[target].notnull()].reset_index(drop = True)
	df = df.iloc[df['smiles'].drop_duplicates(keep = False).index.values]

	y = df[target].values
	drugs = df.smiles.values
	drugs_idx = np.array(['Drug ' + str(i) for i in list(range(len(drugs)))])

	return drugs, y, drugs_idx

def ClinTox_process(name, path, target = None):

	utils.download_unzip(name, path, 'clintox.csv')
	df = pd.read_csv(os.path.join(path,'clintox.csv'))
	df = df.iloc[df['smiles'].drop_duplicates(keep = False).index.values]
	
	y = df["CT_TOX"].values
	drugs = df.smiles.values
	drugs_idx = np.array(['Drug ' + str(i) for i in list(range(len(drugs)))])

	return drugs, y, drugs_idx



import os
import random

import numpy as np
import pandas as pd
from rdkit import Chem
from tqdm import tqdm

tqdm.pandas()


SOURCE_URL = "http://cambridgemedchemconsulting.com/resources/herg_activity_files/pone_data_plus_smiles.txt.zip"
ZIP_FILE_NAME = "data/pone_data_plus_smiles.txt.zip"
TXT_FILE_NAME = "data/pone_data_plus_smiles.txt"
OUT_FILE_NAME = "data/herg_central.csv"

COLUMN_MAP = {
    "PubChem Substance ID": "ID",
    "SMILES": "X",
    "hERG inhibition (%) at 1uM": "hERG_at_1uM",
    "hERG inhibition (%) at 10uM": "hERG_at_10uM",
}


def mol_has_zero_degree_hs(smi):
    mol = Chem.MolFromSmiles(smi)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 1:
            continue
        if atom.GetDegree() == 0:
            return True
    return False


if __name__ == "__main__":
    random.seed(771123)
    np.random.seed(771123)

    if not os.path.exists(ZIP_FILE_NAME):
        os.system(f"wget -P data/ {SOURCE_URL}")
    if not os.path.exists(TXT_FILE_NAME):
        os.system(f"unzip -d data/ {ZIP_FILE_NAME}")

    df = pd.read_csv(TXT_FILE_NAME, sep="\t")
    invalid_idxs = df["SMILES"].progress_apply(mol_has_zero_degree_hs)
    num_removed = sum(invalid_idxs)
    print(f"Removing {num_removed} molecules that have zero-degree hydrogens")
    df = df[~invalid_idxs]
    df["SMILES"] = df["SMILES"].progress_apply(Chem.CanonSmiles)
    df = df.rename(columns=COLUMN_MAP)
    df = df[["ID", "X", "hERG_at_1uM", "hERG_at_10uM"]]
    df["ID"] = df["ID"].astype(str)
    df = df.sample(frac=1)

    # For binary outcome, choose cutoff of IC50 < 10uM
    df["hERG_inhib"] = (df["hERG_at_10uM"] < -50).astype(int)

    print(df.describe())

    df.to_csv(OUT_FILE_NAME, index=False)