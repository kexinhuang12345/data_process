def sabdab_liberis():
	import pickle
	cache_file = '/Users/kexinhuang/Downloads/parapred-master/parapred/precomputed/downloaded_seqs.p'
	with open(cache_file, "rb") as f:
	    output = pickle.load(f)
	pdb2seq = {}
	for x in list(output.keys()):
	    for i, j in output[x].items():
	        seq = ''
	        for a, b in j.items():
	            if a[1] == '':
	                seq += b.lower()
	            else:
	                seq += b
	        pdb2seq[x + '_' + i] = seq
	df = pd.DataFrame(pdb2seq, index = [0]).T.reset_index().rename(columns = {'index': 'ID', 0: 'X'})
	y = []
	for X in df.X.values:
	    y.append([idx for idx, char in enumerate(X) if char.isupper()])
	df['Y'] = y
	df = df[df.Y.apply(lambda x: True if len(x)>0 else False)]
	df.X = df.X.str.upper()
	df.to_pickle('/Users/kexinhuang/Desktop/sabdab_liberis.pkl')