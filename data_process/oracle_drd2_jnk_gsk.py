'''

sklearn 

	1.1.1 
	1.0.2 
	0.24.2 
	0.22.2 

'''

import pickle, sklearn 
from tdc import Oracle 
from tdc.generation import MolGen
data = MolGen(name = 'ZINC')
split = data.get_split()
smiles_lst = split['test']['smiles'].tolist()[:500] 

sklearn_version = sklearn.__version__
print("sklearn_version", sklearn_version)
# ######### drd2 #############
if sklearn_version[:4] == '0.22':
	input_file = 'oracle/drd2_0.pkl' #### raw file 
	model = pickle.load(open(input_file, 'rb'))
	model_params = model.__getstate__()
	del model_params['n_support_'], model_params['probA_'], model_params['probB_']
	pickle.dump(model_params, open('oracle/drd2_tmp.pkl', 'wb'))
	'''
	## 'decision_function_shape', '_impl', 'kernel', 'degree', 'gamma', 'coef0', 'tol', 'C', 'nu', 'epsilon', 
			'shrinking', 'probability', 'cache_size', 'class_weight', 'verbose', 'max_iter', 'random_state', '_sparse', 
			'class_weight_', 'classes_', '_gamma', 'support_', 'support_vectors_', 'n_support_', 'dual_coef_', 'intercept_', 
			'probA_', 'probB_', 'fit_status_', 'shape_fit_', '_intercept_', '_dual_coef_', '_probA', '_probB', '_n_support', '_sklearn_version'
	'''
else:
	# if sklearn_version[:3] == '1.0':
	model_params = pickle.load(open('oracle/drd2_tmp.pkl', 'rb'))
	from sklearn.svm import SVC
	model = SVC()
	for k,v in model_params.items():
		model.__setattr__(k, v)
	pickle.dump(model, open('oracle/drd2.pkl', 'wb'))

	oracle = Oracle('drd2')
	print(oracle(['CC(C)(C)[C@H]1CCc2c(sc(NC(=O)COc3ccc(Cl)cc3)c2C(N)=O)C1', \
        'CCNC(=O)c1ccc(NC(=O)N2CC[C@H](C)[C@H](O)C2)c(C)c1', \
        'C[C@@H]1CCN(C(=O)CCCc2ccccc2)C[C@@H]1O']))
# ######### drd2 #############



######### jnk3 #############
if sklearn_version[:4] == '0.22':
	input_file = 'oracle/jnk3_0.pkl' #### raw file 
	model = pickle.load(open(input_file, 'rb')) ### sklearn.ensemble.forest.RandomForestClassifier
	model_params = model.__getstate__()
	print(model_params.keys())
	del model_params['n_features_']
	pickle.dump(model_params, open('oracle/jnk3_tmp.pkl', 'wb'))
	'''
	['base_estimator', 'n_estimators', 'estimator_params', 'bootstrap', 'oob_score', 'n_jobs', 'random_state', 'verbose', 'warm_start', 'class_weight', 'criterion', 'max_depth', 'min_samples_split', 
			'min_samples_leaf', 'min_weight_fraction_leaf', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split', 'n_features_', 'n_outputs_', 'classes_', 'n_classes_', 
			'base_estimator_', 'estimators_', '_sklearn_version'])
	'''
else:
	# if sklearn_version[:3] == '1.0':
	model_params = pickle.load(open('oracle/jnk3_tmp.pkl', 'rb'))
	from sklearn.ensemble import RandomForestClassifier
	model = RandomForestClassifier()
	for k,v in model_params.items():
		# print(k)
		model.__setattr__(k, v)
	pickle.dump(model, open('oracle/jnk3.pkl', 'wb'))
	oracle = Oracle('jnk3')
	print(oracle(['CC(C)(C)[C@H]1CCc2c(sc(NC(=O)COc3ccc(Cl)cc3)c2C(N)=O)C1', \
        'CCNC(=O)c1ccc(NC(=O)N2CC[C@H](C)[C@H](O)C2)c(C)c1', \
        'C[C@@H]1CCN(C(=O)CCCc2ccccc2)C[C@@H]1O']))
######### jnk3 #############


######### gsk3 #############
if sklearn_version[:4] == '0.22':
	input_file = 'oracle/gsk3b_0.pkl' #### raw file 
	model = pickle.load(open(input_file, 'rb')) ### sklearn.ensemble.forest.RandomForestClassifier
	model_params = model.__getstate__()
	print(model_params.keys())
	del model_params['n_features_']
	pickle.dump(model_params, open('oracle/gsk3b_tmp.pkl', 'wb'))
	'''
	['base_estimator', 'n_estimators', 'estimator_params', 'bootstrap', 'oob_score', 'n_jobs', 'random_state', 'verbose', 'warm_start', 'class_weight', 'criterion', 'max_depth', 'min_samples_split', 
			'min_samples_leaf', 'min_weight_fraction_leaf', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split', 'n_features_', 'n_outputs_', 'classes_', 'n_classes_', 
			'base_estimator_', 'estimators_', '_sklearn_version'])
	'''
else:
	# if sklearn_version[:3] == '1.0':
	model_params = pickle.load(open('oracle/gsk3b_tmp.pkl', 'rb'))
	from sklearn.ensemble import RandomForestClassifier
	model = RandomForestClassifier()
	for k,v in model_params.items():
		# print(k)
		model.__setattr__(k, v)
	pickle.dump(model, open('oracle/gsk3b.pkl', 'wb'))
	oracle = Oracle('gsk3b')
	print(oracle(['CC(C)(C)[C@H]1CCc2c(sc(NC(=O)COc3ccc(Cl)cc3)c2C(N)=O)C1', \
        'CCNC(=O)c1ccc(NC(=O)N2CC[C@H](C)[C@H](O)C2)c(C)c1', \
        'C[C@@H]1CCN(C(=O)CCCc2ccccc2)C[C@@H]1O']))
######### gsk3 #############



