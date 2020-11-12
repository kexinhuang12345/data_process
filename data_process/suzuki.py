import csv, pickle
import pandas as pd 

input_file = "raw_data/suzuki.xlsx"
output_file = "processed_data/suzuki.pkl"



df = pd.read_excel(input_file, sheet_name = 'Sheet1')



print(list(df['Reaction_No']))

# with open(input_file, 'r') as csvfile:
# 	rows = list(csv.reader(csvfile, delimiter = ','))[1:]

# # with open(output_file, 'w') as csvfile:
# # 	fieldnames = ["ID", "X", "Y"]
# # 	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# # 	writer.writeheader()
# # 	for i,row in enumerate(rows):
# # 		reaction_id = "reactions_" + str(i+1)
# # 		reactant, catalyst, product = row[0].split('>')
# # 		reactions_dict = {"reactant": reactant, "catalyst": catalyst, "product": product}
# # 		yields = row[1]
# # 		writer.writerow({'ID': reaction_id, 'X': reactions_dict, 'Y': yields})


# valid_reactions = []
# for i,row in enumerate(rows):
# 	reaction_id = "reactions_" + str(i+1)
# 	reactant, catalyst, product = row[0].split('>')
# 	reactions_dict = {"reactant": reactant, "catalyst": catalyst, "product": product}
# 	yields = row[1]	
# 	lst = [reaction_id, reactions_dict, yields]
# 	valid_reactions.append(lst)

# pickle.dump(valid_reactions, open(output_file, 'wb'))








