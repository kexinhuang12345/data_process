import csv, pickle
import pandas as pd
input_file = "raw_data/buchwald.csv"
# input_file = "raw_data/uspto_raw_head5k.txt"
# output_file = "processed_data/buchwald.csv"
output_file = "processed_data/buchwald.pkl"


with open(input_file, 'r') as csvfile:
	rows = list(csv.reader(csvfile, delimiter = ','))[1:]

# with open(output_file, 'w') as csvfile:
# 	fieldnames = ["ID", "X", "Y"]
# 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 	writer.writeheader()
# 	for i,row in enumerate(rows):
# 		reaction_id = "reactions_" + str(i+1)
# 		reactant, catalyst, product = row[0].split('>')
# 		reactions_dict = {"reactant": reactant, "catalyst": catalyst, "product": product}
# 		yields = row[1]
# 		writer.writerow({'ID': reaction_id, 'X': reactions_dict, 'Y': yields})




reaction_id_lst, reaction_dict_lst, yields_lst = [], [], []

for i,row in enumerate(rows):
	reaction_id = "reactions_" + str(i+1)
	reaction_id_lst.append(reaction_id)
	reactant, catalyst, product = row[0].split('>')
	reactions_dict = {"reactant": reactant, "catalyst": catalyst, "product": product}
	reaction_dict_lst.append(reactions_dict)
	yields = float(row[1])	
	yields_lst.append(yields)



data = {"ID": reaction_id_lst, "X": reaction_dict_lst, "Y": yields_lst}
df = pd.DataFrame(data, columns = ["ID", "X", "Y"])
pickle.dump(df, open(output_file, 'wb'))


# with open(output_file, 'r') as csvfile:
# 	reader = list(csv.reader(csvfile, delimiter=','))[1:]
# 	for row in reader:
# 		reactions_dict = row[1]
# 		print(reactions_dict)







