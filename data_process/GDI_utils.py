def disgenet():
	import pandas as pd
	df = pd.read_csv('/Users/kexinhuang/Downloads/GDA.tsv', sep = '\t')
	df = df[['geneId', 'diseaseId', 'diseaseName', 'score']]

	with open('/Users/kexinhuang/Desktop/GDA_names.txt', 'w') as f:
	    for i in df['geneId'].unique():
	        f.write(str(i))
	        f.write('\n')

	df_gene = pd.read_csv('/Users/kexinhuang/Downloads/uniprot-yourlist_M20201108A94466D2655679D1FD8953E075198DA80E52520.tab', sep = '\t')
	gene2seq = dict(df_gene[['yourlist:M20201108A94466D2655679D1FD8953E075198DA80E25B26', 'Sequence']].values)
	df['geneId'] = df['geneId'].apply(lambda x: str(x))
	df = df[df['geneId'].isin(gene2seq.keys())]
	df['X1'] = [gene2seq[i] for i in df['geneId']]

	import numpy as np 
	import pandas as pd
	with open('/Users/kexinhuang/Downloads/MGDEF.RRF', 'r') as f: 
	    data = f.readlines()
	data = [x.split('|') for x in data]

	id2def = {}
	for i in data[1:]:
	    try:
	        id2def[i[0]] = i[1]
	    except:
	        #print(i)
	        pass

	df['diseaseId'] = df['diseaseId'].apply(lambda x: str(x))
	df = df[df['diseaseId'].isin(id2def.keys())]
	df['X2'] = [id2def[i] for i in df['diseaseId']]
	df['X2'] = [df['diseaseName'].iloc[i] + ': ' + df['X2'].iloc[i] for i in range(len(df))]

	df = df[['geneId', 'X1', 'diseaseId', 'X2', 'score']]
	df.reset_index(drop = True).rename(columns = {'geneId': 'ID1', 'diseaseId': 'ID2', 'score': 'Y'}).to_csv('/Users/kexinhuang/Desktop/disgenet.csv')