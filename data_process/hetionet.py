import json, csv 


input_file = "raw_data/hetionet-v1.0.json"
output_file = "processed_data/hetionet.csv"

with open(input_file, 'r') as f:
	dic = json.load(f)

'''
key:
	'metanode_kinds':   13 types 
			['Anatomy', 'Biological Process', 'Cellular Component', 'Compound', 
			 'Disease', 'Gene', 'Molecular Function', 'Pathway', 
			 'Pharmacologic Class', 'Side Effect', 'Symptom']


	'metaedge_tuples':
			[['Anatomy', 'Gene', 'downregulates', 'both'], ['Anatomy', 'Gene', 'expresses', 'both'], 
			 ['Anatomy', 'Gene', 'upregulates', 'both'], ['Compound', 'Compound', 'resembles', 'both'], 
			 ['Compound', 'Disease', 'palliates', 'both'], ['Compound', 'Disease', 'treats', 'both'], 
			 ['Compound', 'Gene', 'binds', 'both'], ['Compound', 'Gene', 'downregulates', 'both'], 
			 ['Compound', 'Gene', 'upregulates', 'both'], ['Compound', 'Side Effect', 'causes', 'both'], 
			 ['Disease', 'Anatomy', 'localizes', 'both'], ['Disease', 'Disease', 'resembles', 'both'], 
			 ['Disease', 'Gene', 'associates', 'both'], ['Disease', 'Gene', 'downregulates', 'both'], 
			 ['Disease', 'Gene', 'upregulates', 'both'], ['Disease', 'Symptom', 'presents', 'both'], 
			 ['Gene', 'Biological Process', 'participates', 'both'], ['Gene', 'Cellular Component', 'participates', 'both'], 
			 ['Gene', 'Gene', 'covaries', 'both'], ['Gene', 'Gene', 'interacts', 'both'], 
			 ['Gene', 'Gene', 'regulates', 'forward'], 
			 ['Gene', 'Molecular Function', 'participates', 'both'], ['Gene', 'Pathway', 'participates', 'both'], 
			 ['Pharmacologic Class', 'Compound', 'includes', 'both']]

	'kind_to_abbrev', 
			{'Biological Process': 'BP', 'Cellular Component': 'CC', 'causes': 'c', 
			 'Pharmacologic Class': 'PC', 'Molecular Function': 'MF', 'palliates': 'p', 
			 'downregulates': 'd', 'expresses': 'e', 'Gene': 'G', 'covaries': 'c', 
			 'upregulates': 'u', 'presents': 'p', 'Anatomy': 'A', 'Symptom': 'S', 
			 'Pathway': 'PW', 'treats': 't', 'localizes': 'l', 'Disease': 'D', 
			 'participates': 'p', 'binds': 'b', 'includes': 'i', 'associates': 'a', 
			 'Compound': 'C', 'interacts': 'i', 'resembles': 'r', 'regulates': 'r', 'Side Effect': 'SE'}
'''

'''
	'nodes',   47031 elements, each is a dict. 
			{'kind': 'Molecular Function', 'identifier': 'GO:0031753', 
			 'name': 'endothelial differentiation G-protein coupled receptor binding', 
			 'data': {'source': 'Gene Ontology', 'license': 'CC BY 4.0', 'url': 'http://purl.obolibrary.org/obo/GO_0031753'}}

			{'kind': 'Side Effect', 'identifier': 'C0023448', 
			 'name': 'Lymphocytic leukaemia', 
			 'data': {'source': 'UMLS via SIDER 4.1', 'license': 'CC BY-NC-SA 4.0', 'url': 'http://identifiers.org/umls/C0023448'}}
'''


############ pass ############
# node_lst = dic['nodes']
# for node in node_lst:
# 	assert 'kind' in node
# 	assert 'name' in node 
# 	assert 'data' in node
############ pass ############

'''
	'edges',   2250197 elements, 
			{'source_id': ['Anatomy', 'UBERON:0000178'], 
			 'target_id': ['Gene', 9489], 
			 'kind': 'upregulates', 
			 'direction': 'both', 
			 'data': {'source': 'Bgee', 'unbiased': True}}


			{'source_id': ['Anatomy', 'UBERON:0000992'], 
			 'target_id': ['Gene', 9816], 
			 'kind': 'expresses', 
			 'direction': 'both', 
			 'data': {'sources': ['Bgee'], 'unbiased': True}}
 

 			{'source_id': ['Anatomy', 'UBERON:0002450'], 
 			 'target_id': ['Gene', 55093], 
 			 'kind': 'expresses', 
 			 'direction': 'both', 
 			 'data': {'sources': ['Bgee'], 'unbiased': True}}


			{'source_id': ['Gene', 153129], 
			 'target_id': ['Cellular Component', 'GO:0005770'], 
			 'kind': 'participates', 
			 'direction': 'both', 
			 'data': {'source': 'NCBI gene2go', 'license': 'CC BY 4.0', 'unbiased': False}}

'''

############ pass ############
# edges = dic['edges']
# for edge in edges:
# 	assert 'source_id' in edge
# 	assert 'target_id' in edge 
# 	assert 'kind' in edge 
# 	assert 'direction' in edge 
# 	assert 'data' in edge 
############ pass ############

fieldnames = ['source_type', 'source_id', 'target_type', 'target_id', 'type', 'direction']
edges = dic['edges']
with open(output_file, 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader() 

	for edge in edges:
		line_dict = {}
		line_dict['source_type'] = edge['source_id'][0]
		line_dict['source_id'] = str(edge['source_id'][1])
		line_dict['target_type'] = edge['target_id'][0]
		line_dict['target_id'] = str(edge['target_id'][1])
		line_dict['type'] = edge['kind']
		line_dict['direction'] = edge['direction']
		writer.writerow(line_dict)






















