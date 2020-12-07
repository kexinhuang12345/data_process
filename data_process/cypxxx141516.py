import csv, os 
import pandas as pd


input_folder = 'raw_data'
output_folder = 'processed_data'

names = ['cyp2c9', 'cyp2d6', 'cyp3a4']



append_name = '_substrate_carbonmangels.csv'


for name in names:
	input_file = os.path.join(input_folder, "minf_201100069_sm_" + name + "subs.xls")
	output_file = os.path.join(output_folder, name + append_name)
	# assert os.path.exists(input_file)
	df = pd.read_excel(input_file)
	# print(df.keys())	
	X = list(df['SMILES'])
	ID = list(df[name.upper() + ' compound'])
	Y = list(df['substrate'])
	Y = list(map(lambda x:1 if int(x)==1 else 0, Y))
	with open(output_file, 'w') as csvfile:
		fieldnames = ['ID', 'X', 'Y']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for x,y,iid in zip(X,Y,ID):
			writer.writerow({'ID':iid, 'X':x, 'Y':y})



