import csv, os 
import pandas as pd


input_file = 'raw_data/TX-006-C7TX00144D-s001.xlsx'
output_folder = 'processed_data'

def strip_lst(lst_of_stirng):
	return list(map(lambda x:x.strip(), lst_of_stirng))


### RT ###
RT_df1 = pd.read_excel(open(input_file, 'rb'), sheet_name = 'RT_train')
RT1_X = list(RT_df1['Unnamed: 2'])[2:]
RT1_labelnames = list(RT_df1['Unnamed: 4'])[2:]
RT1_ID = list(RT_df1['Unnamed: 1'])[2:]

RT_df2 = pd.read_excel(open(input_file, 'rb'), sheet_name = 'RT_test')
RT2_X = list(RT_df2['Unnamed: 2'])[1:]
RT2_labelnames = list(RT_df2['Unnamed: 4'])[1:]
RT2_ID = list(RT_df2['Unnamed: 1'])[1:]

RT_X = strip_lst(RT1_X + RT2_X)
RT_labelnames = RT1_labelnames + RT2_labelnames
RT_ID = RT1_ID + RT2_ID 
RT_output_file = os.path.join(output_folder, "rainbow_trout_li.csv")
### RT ###


### LP ### 
LP_df1 = pd.read_excel(open(input_file, 'rb'), sheet_name = 'LP_train')
LP1_X = list(LP_df1['Unnamed: 2'])[1:]
LP1_labelnames = list(LP_df1['Unnamed: 4'])[1:]
LP1_ID = list(LP_df1['Unnamed: 1'])[1:]

LP_df2 = pd.read_excel(open(input_file, 'rb'), sheet_name = 'LP_test')
LP2_X = list(LP_df2['Unnamed: 2'])[1:]
LP2_labelnames = list(LP_df2['Unnamed: 4'])[1:]
LP2_ID = list(LP_df2['Unnamed: 1'])[1:]

LP_X = strip_lst(LP1_X + LP2_X) 
LP_labelnames = LP1_labelnames + LP2_labelnames 
LP_ID = LP1_ID + LP2_ID
LP_output_file = os.path.join(output_folder, "lepomis_li.csv")
### LP ### 


labelname2label = {"Very highly toxic": 4,
				   "Highly toxic": 3,
				   "Moderately toxic": 2,
				   "Slightly toxic": 1, 
				   "Nontoxic": 0,
				   }

def df2outputfile(X, ID, labelnames, output_file):
	Y = list(map(lambda x:labelname2label[x], labelnames))
	with open(output_file, 'w') as csvfile:
		fieldnames = ['ID', 'X', 'Y', 'Map']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for x,y,iid,labelname in zip(X,Y,ID,labelnames):
			writer.writerow({"ID":iid, "X":x, "Y":y, "Map":labelname})

df2outputfile(RT_X, RT_ID, RT_labelnames, RT_output_file)
df2outputfile(LP_X, LP_ID, LP_labelnames, LP_output_file)





