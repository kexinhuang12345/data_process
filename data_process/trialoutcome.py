import csv 

date_file = 'nctid_date.txt'
raw_file = "raw_data.csv"
phase1_file = 'phase1.tab'
phase2_file = 'phase2.tab'
phase3_file = 'phase3.tab' 

from collections import defaultdict
nctid2date = defaultdict(lambda x:('NA', 'NA'))
with open(date_file, 'r') as fin:
	lines = fin.readlines()
	for line in lines:
		line = line.strip().split('\t')
		nctid2date[line[0]] = line[1], line[2]

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
	    writer = csv.writer(csvfile, delimiter='\t')
	    writer.writerow(['nctid', 'start_date', 'complete_date', 'drug_molecules', 'icdcodes', 'eligibility_criteria', 'Y'])
	    for i,line in enumerate(lines):
	    	nctid = line[0]
	    	start_date = nctid2date[nctid][0]
	    	complete_date = nctid2date[nctid][1]
	    	drug = line[8][2:-2].split("', '")
	    	drug = '__'.join(drug)
	    	label = line[3]
	    	icdcodes = line[6][2:-2]
	    	icdcodes = ''.join(list(filter(lambda x:x!='[' and x!=']' and x!='"' and x!="'", icdcodes)))
	    	icdcodes = '__'.join(icdcodes.split(', '))
	    	criteria = line[9]
	    	criteria = ' '.join(criteria.split('\n'))
	    	for t in range(5):
	    		criteria = ' '.join(criteria.split('  ')) #### remove multiple spaces. 
	    	writer.writerow([nctid, start_date, complete_date, drug, icdcodes, criteria, label])
	    	# writer.writerow([str(i), str(i), str(i), drug, icdcodes, criteria, label])




