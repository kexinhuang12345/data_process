import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

data = pd.read_pickle('./drugcomb_mean_genomic_feats.pkl')
train_set, val_test_set = train_test_split(data, train_size=0.7)
val_set, test_set = train_test_split(val_test_set, train_size=0.33)

# Get tissue information
tissue_df = pd.read_csv('./NCI_60_tissues.csv')
tissue_df = tissue_df.append({'Cell Line': 'MCF7', 'Tissue': 'breast'},
                             ignore_index=True)
tissue_data_df = data.merge(tissue_df, left_on='Cell_Line_ID',
                            right_on='Cell Line')
tissue_data_df['concat1'] = tissue_data_df['Drug1_ID'] + ',' + tissue_data_df[
    'Drug2_ID']

# Get shared combinations across all tissues
all_tissues = tissue_data_df['Tissue'].unique()
data['concat1'] = data['Drug1_ID'] + ',' + data['Drug2_ID']

combinations = []
for c in data['Cell_Line_ID'].unique():
    df = data[data['Cell_Line_ID'] == c]
    combos = np.concatenate([df['concat1'].values])
    combinations.append(set(combos))

intxn = combinations[0]
for c in combinations:
    intxn = intxn.intersection(c)

# Select unique drug combinations for test and validation dataset 
test_choices = np.random.choice(list(intxn),
                                int(len(test_set) / len(
                                    data['Cell_Line_ID'].unique())),
                                replace=False)
trainval_intxn = intxn.difference(test_choices)
val_choices = np.random.choice(list(trainval_intxn),
                               int(len(val_set) / len(
                                   data['Cell_Line_ID'].unique())),
                               replace=False)

## Create train and test set
test_set = tissue_data_df[tissue_data_df['concat1'].isin(test_choices)]
val_set = tissue_data_df[tissue_data_df['concat1'].isin(val_choices)]
train_set = tissue_data_df[
    ~tissue_data_df['concat1'].isin(test_choices)].reset_index(drop=True)
train_set = train_set[~train_set['concat1'].isin(val_choices)]


# train_set, val_set = train_test_split(train_set, test_size=0.125)


# Data splitting by metric
def write_train_val_test(train, val, test, m, dirname, only_test=False,
                         include_cols=[]):
    cols = ['Drug1_ID', 'Drug2_ID', 'Cell_Line_ID', 'Drug1', 'Drug2',
            'CellLine', m] + include_cols
    if not only_test:
        train.loc[:, cols].rename(columns={m: 'Y'}).to_pickle(
            dirname + '/train.pkl')
        val.loc[:, cols].rename(columns={m: 'Y'}).to_pickle(
            dirname + '/valid.pkl')
    test.loc[:, cols].rename(columns={m: 'Y'}).to_pickle(dirname + '/test.pkl')


# Write output to file
metrics = ['CSS', 'Synergy_ZIP', 'Synergy_Bliss', 'Synergy_Loewe',
           'Synergy_HSA']
home_dir = '../data/drugsyn_group/drugcomb_'
for m in metrics:
    if not os.path.exists(home_dir + m):
        os.makedirs(home_dir + m)
    if m == 'CSS':
        cols = ['target_class']
        train_set = train_set.rename(columns={'Tissue': 'target_class'})
        val_set = val_set.rename(columns={'Tissue': 'target_class'})
        test_set = test_set.rename(columns={'Tissue': 'target_class'})
    else:
        cols = []
    write_train_val_test(train_set, val_set, test_set, m,
                         dirname=home_dir + m + '/', include_cols=cols)