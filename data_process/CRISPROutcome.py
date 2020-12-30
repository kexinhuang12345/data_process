# Pre processing script for CRISPR outcomes dataset (Leenay 2019)
# ---------
# T-Cell outcome analysis data available at:
# https://figshare.com/articles/dataset/Analyzed_T-Cell_DNA_Repair_Outcomes/6957125
# For CrispRVariants analysis output: LeenayIndelCounts.tar.gz
# For sequence information: Leenay_bam_df.rds (converted to csv below)
# ---------

import pandas as pd
import numpy as np
import glob
from scipy.stats import entropy
from collections import defaultdict


def get_guide_seq(ref_seq):
    """ 
    Read in guide sequence
    """

    guide_seq = ref_seq[13:36]
    if guide_seq[-2:] != 'GG':
        print('incorrect alignment')
        return -1
    return guide_seq


def count_frameshifts(count_df):
    """
    Given a CrispRVariants outcome analysis file, 
    count number of frameshifts
    """

    fs = []
    for v in count_df.index:
        if v == 'no variant': continue;
        if v == 'Other': continue;
        if v[:3] == 'SNV': continue;
        indels = v.split(',')
        checks = []
        for x in indels:
            checks.append(int(x.split(':')[1][:-1]) % 3 != 0)
        if all(checks):
            fs.append(v)

    return count_df.loc[fs].sum()


def avg_indel_length(df, ins=False, dele=False):
    """
    Given a CrispRVariants outcome analysis file, count average lenght of 
    insertion/deletions
    """

    lengths = defaultdict(int)

    for x in get_indels(df, ins=ins, dele=dele):

        l = x.split(':')[:-1]
        if len(l) == 1:
            lengths[np.abs(int(l[0]))] += df.loc[x]

    avg = 0
    for k, v in lengths.items():
        avg += k * v
    try:
        avg = avg / sum(lengths.values())
    except:
        return 0

    return avg


def check_read_count(df):
    """
    Given a CrispRVariants outcome analysis file, check if there are enough 
    reads
    """

    return df.sum() > 1000


def get_indels(count_df, ins=False, dele=False):
    """
    Given a CrispRVariants outcome analysis file, get list of all 
    indels/insertions/deletions
    """

    if ins:
        if dele:
            return [v for v in count_df.index if v[-1] == 'I' or v[-1] == 'D']
        else:
            return [v for v in count_df.index if v[-1] == 'I']
    elif dele:
        return [v for v in count_df.index if v[-1] == 'D']


def get_entropy(count_df):
    """
    Given a CrispRVariants outcome analysis file, comput the entopy of the 
    indels
    """

    return entropy(count_df.loc[get_indels(count_df, True, True)])


def update_metrics(counts_df, metrics, guide_seq, k=0):
    """
    Given a CrispRVariants outcome analysis file, and a chosen guide 
    sequence, update metrics dictionary
    """

    for donor, donor_name in enumerate(counts_df.columns):

        donor_name = donor_name.split('_')[0]
        metrics[guide_seq] = defaultdict(int)
        donor_df = counts_df.iloc[:, donor]

        try:
            donor_df = donor_df.drop('no variant');
        except:
            pass;

        # remove sites with less than 1000 reads
        if check_read_count(donor_df) == False:
            continue

        # indel count
        all_outcomes = donor_df
        num_indels = donor_df.loc[get_indels(donor_df, ins=True, 
                                             dele=True)].sum()
        num_ins = donor_df.loc[get_indels(donor_df, ins=True)].sum()
        metrics[guide_seq]['Fraction_Insertions'] = num_ins / num_indels

        # insertion length
        metrics[guide_seq]['Avg_Insertion_Length'] = avg_indel_length(
            donor_df, ins=True)

        # deletion length
        metrics[guide_seq]['Avg_Deletion_Length'] = avg_indel_length(
            donor_df, dele=True)

        # entropy
        metrics[guide_seq]['Indel_Diversity'] = get_entropy(donor_df)

        # frameshifts
        metrics[guide_seq]['Fraction_Frameshifts'] = count_frameshifts(
            donor_df) / donor_df.sum()

        # For each guideRNA we only look at one donor because
        # the paper claims repair outcomes do not depend on donor
        if donor >= k:
            break


def main():
    """
    main function for producing TDC dataset
    """

    df = pd.read_csv('Leenay_bam_df.csv')
    df = df.dropna()
    df = df.drop_duplicates(subset='reference')

    metrics = {}
    for gene in df['genename'].values:

        if gene[:3] == 'NTC':
            continue
        if gene[-3:] == 'r80':
            continue

        # Get guide sequence
        ref_seq = df[df['genename'] == gene]['reference'].values[0]
        guide_seq = get_guide_seq(ref_seq)

        if guide_seq == -1: continue;

        # For each replicate
        for repeat in glob.glob('./counts/counts-' + gene + '-*.txt'):
            counts_df = pd.read_csv(repeat)

            # Update the metrics
            update_metrics(counts_df, metrics, guide_seq)

    metrics = pd.DataFrame(metrics).T.dropna()
    metrics = metrics.reset_index().rename(columns={'index': 'GuideSeq'})
    metrics.to_csv('metrics.csv')


"""
Additional information:
control_genes = ['CDK9r', 'CDK9r80', 'CXCR4r', 'CXCR4r80', 'LEDGFr', 'LEDGFr80', 'NTC']
all_donors = ['RL384-00015', 'RL384-00017', 'RL384-00018', 'RL384-00019',
       'RL384-00020', 'RL384-00021', 'RL384-00022', 'RL384-00023',
       'RL384-00024', 'RL384-00025', 'RL384-00026', 'RL384-00027',
       'RL384-00028', 'RL384-00029', 'RL384-00033']
"""
