import pandas as pd

d = pd.read_csv('/Users/kexinhuang/Downloads/chembl_29_chemreps.txt', sep = '\t')
d = d[['chembl_id', 'canonical_smiles']]
d = d.rename(columns = {'chembl_id': 'ID', 
                   'canonical_smiles': 'smiles'})

d = d.drop_duplicates()
from rdkit import Chem

def catch_bug(x):
    try: 
        return Chem.MolToSmiles(Chem.MolFromSmiles(x))
    except:
        return 'NULL'

d['smiles'] = d.smiles.apply(lambda x: catch_bug(x)).values

d = d[d.smiles != 'NULL'].reset_index(drop = True)