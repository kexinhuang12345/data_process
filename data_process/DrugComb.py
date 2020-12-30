"""
Script for writing DrugComb data in the correct format for TDC
@yhr91
"""

import pandas as pd
import pubchempy as pcp
import numpy as np
from collections import defaultdict

def get_SMILES(cname):
    """
    Retrieve canonical SMILES for all compounds
    NOTE: This function returns the shortest of all canonical SMILES!
    """
    print(cname)
    smiles_list = [s.canonical_smiles for s in pcp.get_compounds(cname, 'name')]
    lens = [len(item) for item in smiles_list]
    try:
       return smiles_list[np.argmin(lens)]
    except:
       return np.nan
    
def get_feat_dict(path, start_col):
    """
    Get dictionary of features for each cell line
    """
    feat_df = pd.read_excel(path, header=10)
    feat_df.columns = [name.split(':')[-1] for name in feat_df.columns]

    feat_df = feat_df.rename(columns = {'HCT-116':'HCT116', 'UACC-62':'UACC62',
                'A549/ATCC': 'A549', 'NCI-H23':'NCIH23', 'OVCAR-3':'OVCAR3'})

    feat_dict = defaultdict(lambda: np.nan)
    for col in feat_df.columns[start_col:]:
        feat_dict[col] = feat_df.loc[:,col].values
    return feat_dict

def main():
    # DrugComb: Summary table
    drugcomb = pd.read_csv('summary_table_v1.4.csv')
    drugcomb_subset_mean = pd.read_csv('drugcomb_subset_mean.csv')
    
    # Subset columns
    drugcomb_subset = drugcomb.dropna(0).loc[:,['drug_row', 'drug_col', 
                                'cell_line_name', 'css', 'synergy_zip', 
                                'synergy_bliss', 'synergy_loewe', 'synergy_hsa']]
    
    # Take the average across replicates
    drugcomb_subset_mean = drugcomb_subset.groupby(['drug_row','drug_col',
                                            'cell_line_name']).mean().reset_index()
    
    # Create a SMILES mapping dictionary
    all_cmpds = list(set(drugcomb_subset.drug_row.values).union(set(
                        drugcomb_subset.drug_col.values)))
    smiles_map = {c:get_SMILES(c) for c in all_cmpds}
    
    
    # Create new columns for SMILES
    drugcomb_subset_mean['smiles_row'] = [smiles_map[v] 
                                    for v in drugcomb_subset_mean.drug_row.values]
    drugcomb_subset_mean['smiles_col'] = [smiles_map[v] 
                                    for v in drugcomb_subset_mean.drug_col.values]
    
    # Rename columns
    drugcomb_subset_mean = drugcomb_subset_mean.rename(
        columns={'drug_row':'Drug1_ID', 'drug_col':'Drug2_ID',
                 'cell_line_name':'Cell_Line_ID',
                 'smiles_row':'Drug1_SMILES', 'smiles_col':'Drug2_SMILES'})
    drugcomb_subset_mean.to_csv('drugcomb_subset_mean.csv')
    
    # Get all cell line names
    drugcomb_cell_lines = drugcomb_subset_mean['Cell_Line_ID'].unique()
    
    # Create a dictionary for each genomic feature type
    protein_feats = get_feat_dict('./NCI/Protein__SWATH_(Mass_spectrometry)_Protein.xls',
                                  start_col=9)
    expression_feats = get_feat_dict('./NCI/RNA__RNA_seq_composite_expression.xls',
                                  start_col=6)
    microRNA_feats = get_feat_dict('./NCI/RNA__microRNA_OSU_V3_chip_log2.xls',
                                  start_col=9)
    
    # Add genomic feature columns to the dataframe
    drugcomb_subset_mean['protein_feats'] = [protein_feats[v] 
                            for v in drugcomb_subset_mean['Cell_Line_ID'].values]
    drugcomb_subset_mean['expression_feats'] = [expression_feats[v] 
                            for v in drugcomb_subset_mean['Cell_Line_ID'].values]
    drugcomb_subset_mean['microRNA_feats'] = [microRNA_feats[v] 
                            for v in drugcomb_subset_mean['Cell_Line_ID'].values]
    
    # Drop NaN values
    drugcomb_subset_mean = drugcomb_subset_mean.dropna(0)
    
    # Rename columns
    drugcomb = drugcomb.reset_index(drop=True)
    drugcomb = drugcomb.rename(columns = {'css':'CSS', 'synergy_zip':'Synergy_ZIP',
                               'synergy_bliss': 'Synergy_Bliss',
                               'synergy_loewe': 'Synergy_Loewe', 
                               'synergy_hsa': 'Synergy_HSA',
                               'protein_feats': 'CellLine_Feat_Proteome',
                               'Drug1_SMILES':'Drug1', 'Drug2_SMILES':'Drug2',
                               'expression_feats': 'CellLine_Feat_Expression',
                               'microRNA_feats': 'CellLine_Feat_microRNA'})
    
    # Create a single column for cell line features
    CellLineFeats = []
    for idx, item in drugcomb.iterrows():
        CellLineFeats.append([item['CellLine_Feat_Expression'],
                              item['CellLine_Feat_Proteome'],
                              item['CellLine_Feat_microRNA']])
    drugcomb['CellLine'] = CellLineFeats
    drugcomb = drugcomb.drop(['CellLine_Feat_Expression','CellLine_Feat_microRNA',
                              'CellLine_Feat_Proteome'], axis=1)
    
    # Save dataframe to a pickle
    drugcomb_subset_mean.to_pickle('drugcomb_mean_genomic_feats.pkl')
    
if __name__ == '__main__':
    main()
