import csv 

raw_file = "raw_data.csv"
phase1_file = 'phase1.csv'
phase2_file = 'phase2.csv'
phase3_file = 'phase3.csv' 

with open(raw_file, 'r') as csvfile:
	reader = list(csv.reader(csvfile, delimiter=','))

header = reader[0]
reader = reader[1:]
print(header)
# ['nctid', 'status', 'why_stop', 'label', 'phase', 'diseases', 'icdcodes', 'drugs', 'smiless', 'criteria']

phase1_lines = list(filter(lambda x:'1' in x[4], reader))
phase2_lines = list(filter(lambda x:'2' in x[4], reader))
phase3_lines = list(filter(lambda x:'3' in x[4], reader))

print(len(phase1_lines), len(phase2_lines), len(phase3_lines))


paired_data = [(phase1_file, phase1_lines), (phase2_file, phase2_lines), (phase3_file, phase3_lines)]

for file, lines in paired_data:
	with open(file, 'w', newline='') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',')
	    writer.writerow(['ID1', 'ID2', 'X1', 'X2', 'Y'])
	    for i,line in enumerate(lines):
	    	drug = line[8][2:-2].split("', '")
	    	drug = '__'.join(drug)
	    	# print(type(drug), drug)
	    	label = line[3]
	    	icdcodes = line[6][2:-2]
	    	icdcodes = ''.join(list(filter(lambda x:x!='[' and x!=']' and x!='"' and x!="'", icdcodes)))
	    	icdcodes = '__'.join(icdcodes.split(', '))
	    	# print(icdcodes)
	    	writer.writerow([str(i), str(i), drug, icdcodes, label])




