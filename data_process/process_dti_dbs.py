import logging

import pandas
from Bio import SeqIO

logger = logging.getLogger(__name__)


def get_chembl_smiles(chembl_ids, chembl_smiles_file):
    molecules = pandas.read_csv(chembl_smiles_file, sep='\t').set_index('chembl_id').T.to_dict()
    smiles_list = []
    for chembl_id in chembl_ids:
        if chembl_id in molecules:
            smiles_list.append(molecules[chembl_id]['canonical_smiles'])
        else:
            smiles_list.append(None)
    return smiles_list


def get_uniprot_proteins(uniprot_ids, uniprot_homo_sapiens_file_path):
    sequences = read_uniprot(uniprot_homo_sapiens_file_path)
    s = []
    for uniprot_id in uniprot_ids:
        if uniprot_id and (uniprot_id in sequences):
            s.append(sequences[uniprot_id]['sequence'])
        else:
            logger.warning('Omitting protein %s'%uniprot_id)
            s.append(None)
    return s



def read_uniprot(path):
    fasta_iterator = SeqIO.parse(path, "fasta")
    seqs = {}
    for seq in fasta_iterator:
        s = seq.format("fasta")
        uniprot_id = s.split('|')[1]
        name = s.split('|')[2].split('OS')[0].strip().replace('\r','')
        sequence = s.split('\n', 1)[1].replace('\r','').replace('\n','')
        seqs[uniprot_id] = {'name':name, 'sequence': sequence}
    return seqs


def process_dtc(dtc_path, standard_type, uniprot_homo_sapiens_file_path, chembl_smiles_file):
    drug_ids = []
    protein_ids = []
    labels = []
    standards = []
    with pandas.read_csv(dtc_path, chunksize=5* 10 ** 5, keep_default_na=False) as reader:
        for chunk in reader:
            if standard_type == 'activity_comment':
                for i, row in chunk.dropna().iterrows():
                    standard = row[standard_type]
                    if standard:
                        standard = standard.lower()
                        if ('inactive' in standard) or ('not active' in standard):
                            drug_ids.append(row['compound_id'])
                            protein_ids.append(row['target_id'])
                            labels.append(0)
                        elif ('active' in standard) or ('inhibitor' in standard) or ('antagonist' in standard) or ('agonist' in standard):
                            drug_ids.append(row['compound_id'])
                            protein_ids.append(row['target_id'])
                            labels.append(1)
            else:
                for i, row in chunk.iterrows():
                    standard = row['standard_type']
                    if standard and standard_type in standard.lower():
                        standard = standard.lower()
                        standards.append(standard)
                        try:
                            standard_value = float(row['standard_value'])
                        except:
                            continue
                        if row['standard_units'] == 'NM' and row['standard_relation'] in ('=', '==', '<', '<='):
                            labels.append(standard_value)
                            drug_ids.append(row['compound_id'])
                            protein_ids.append(row['target_id'])
    chembl_smiles = get_chembl_smiles(drug_ids, chembl_smiles_file=chembl_smiles_file)
    protein_sequences = get_uniprot_proteins(protein_ids, uniprot_homo_sapiens_file_path=uniprot_homo_sapiens_file_path)
    df = pandas.DataFrame({'ID2':protein_ids, 'X2': protein_sequences,'ID1': drug_ids , 'X1': chembl_smiles, 'Y': labels})
    logger.info(len(df))
    df.dropna(inplace=True)
    logger.info(len(df))
    df = df.drop_duplicates()
    logger.info(len(df))
    df.to_csv('data/dtc_'+standard_type+'.tab', sep='\t')
    return df


if __name__ == '__main__':
    for standard_type in ['ic50','ec50', 'ki', 'kd', 'activity_comment']:
        df = process_dtc(dtc_path='dataset/DtcDrugTargetInteractions.csv',
                         standard_type=standard_type,
                         uniprot_homo_sapiens_file_path='dataset/uniprot_human.fasta',
                         chembl_smiles_file='dataset/chembl_ids_smiles.tsv'
                         )
