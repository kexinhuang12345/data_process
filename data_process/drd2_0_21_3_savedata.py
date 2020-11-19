import pickle 
import sklearn 



if sklearn.__version__ == "0.21.3":
	input_oracle = "oracle/drd2.pkl"
	median_oracle = "oracle/drd2_median.pkl"

	svc_obj = pickle.load(open(input_oracle, 'rb'))
	svc_obj.__setattr__('_probA', svc_obj.probA_)
	svc_obj.__setattr__('_probB', svc_obj.probB_)
	svc_obj.__setattr__('_n_support', svc_obj.n_support_)
	pickle.dump(svc_obj, open(median_oracle, 'wb'))




'''

from tdc.oracles import Oracle 
oracle = Oracle(name = 'drd2')
oracle('CCC')

'''












'''
	set_params


pip install scikit-learn==0.21.3 

pip install scikit-learn==0.23.2 





['decision_function_shape', '_impl', 'kernel', 'degree', 'gamma', 'coef0', 'tol', 'C', 'nu', 
'epsilon', 'shrinking', 'probability', 'cache_size', 'class_weight', 'verbose', 
'max_iter', 'random_state', '_sparse', 'class_weight_', 'classes_', '_gamma', 
'support_', 'support_vectors_', 'n_support_', 'dual_coef_', 'intercept_', 
'probA_', 'probB_', 'fit_status_', 'shape_fit_', '_intercept_', '_dual_coef_', 
'__module__', '__doc__', '__init__', '__abstractmethods__', '_abc_impl', 
'_validate_targets', 'decision_function', 'predict', '_check_proba', 
'predict_proba', '_predict_proba', 'predict_log_proba', '_predict_log_proba', 
'_dense_predict_proba', '_sparse_predict_proba', '_get_coef', '_estimator_type', 
'score', '_more_tags', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', 
'__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', 
'__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', 
'__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', 
'__class__', '_sparse_kernels', '_pairwise', 'fit', '_warn_from_fit_status', '_dense_fit', 
'_sparse_fit', '_dense_predict', '_sparse_predict', '_compute_kernel', '_decision_function', 
'_dense_decision_function', '_sparse_decision_function', '_validate_for_predict', 'coef_', '_get_param_names', 
'get_params', 'set_params', '__getstate__', '__setstate__', '_get_tags', '_check_n_features', 
'_validate_data', '_repr_html_', '_repr_html_inner', '_repr_mimebundle_']





['decision_function_shape', '_impl', 'kernel', 'degree', 'gamma', 'coef0', 'tol', 'C', 'nu',
'epsilon', 'shrinking', 'probability', 'cache_size', 'class_weight', 'verbose',
'max_iter', 'random_state', '_sparse', 'class_weight_', 'classes_', '_gamma', 
'support_', 'support_vectors_', 'n_support_', 'dual_coef_', 'intercept_',
'probA_', 'probB_', 'fit_status_', 'shape_fit_', '_intercept_', '_dual_coef_',
'__module__', '__doc__', '__init__', '__abstractmethods__', '_abc_impl',
'_validate_targets', 'decision_function', 'predict', '_check_proba', 
'predict_proba', '_predict_proba', 'predict_log_proba', '_predict_log_proba', 
'_dense_predict_proba', '_sparse_predict_proba', '_get_coef', '_estimator_type', 
'score', '_more_tags', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', 
'__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_sparse_kernels', '_pairwise', 'fit', '_warn_from_fit_status', '_dense_fit', '_sparse_fit', '_dense_predict', '_sparse_predict', '_compute_kernel', '_decision_function', '_dense_decision_function', '_sparse_decision_function', '_validate_for_predict', 'coef_', '_get_param_names', 'get_params', 'set_params', '__getstate__', '__setstate__', '_get_tags', '_check_n_features', '_validate_data', '_repr_html_', '_repr_html_inner', '_repr_mimebundle_']













'''


