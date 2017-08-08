import numpy as np
import pdb
import scipy.io
import tensorflow as tf
from keras.callbacks import TensorBoard

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt


class output_cc:
	input_train_perm = np.array([])
	output_train_perm = np.array([])
	input_valid_perm = np.array([])
	output_valid_perm = np.array([])
	input_test_perm = np.array([])

	input_train = np.array([])
	input_valid = np.array([])
	input_test = np.array([])
	output_valid = np.array([])
	
	indices_input_samples_train_perm = np.array([])
	indices_ouput_samples_train_perm = np.array([])
	indices_input_samples_test_perm = np.array([])
	
	indices_classI_samples_train = np.array([])
	indices_classI_samples_test = np.array([])
	indices_classJ_samples_test = np.array([])
	indices_classI_samples_valid = np.array([])

	def function(self):
		print("This is output_cc class")

class input_cc:
	classI = []
	classJ = []
	train_valid_split = np.array([])
	visual_features = np.array([])
	dataset_labels = np.array([])
        min_num_samples_per_class = []

	def function(self):
		print("This is input_cc class")

def function_get_training_data_cc(obj_input_cc):
	#pdb.set_trace()
	classI = obj_input_cc.classI
	classJ = obj_input_cc.classJ
	TR_TS_VA_SPLIT = obj_input_cc.train_valid_split
	dataset_labels = obj_input_cc.dataset_labels
	visual_features_dataset = obj_input_cc.visual_features

	print "************* Class %d >>> Class %d *************************"%(classI, classJ)
	MIN_NUMBER_OF_SAMPLES_OF_CLASS = obj_input_cc.min_num_samples_per_class #51 # class27 51 samples for apy class 1-32: 30

	indices_classI_samples = np.flatnonzero(dataset_labels == classI)
	indices_classJ_samples = np.flatnonzero(dataset_labels == classJ)

	if classI == classJ:
		number_of_samples_classI_for_train = int(TR_TS_VA_SPLIT[0] * np.size(indices_classI_samples))
		number_of_samples_classJ_for_train = int(TR_TS_VA_SPLIT[0] * np.size(indices_classJ_samples))
	else: 	
		number_of_samples_classI_for_train = int(TR_TS_VA_SPLIT[0] * MIN_NUMBER_OF_SAMPLES_OF_CLASS)
		number_of_samples_classJ_for_train = int(TR_TS_VA_SPLIT[0] * MIN_NUMBER_OF_SAMPLES_OF_CLASS)
	
	indices_classI_samples_train = indices_classI_samples[:number_of_samples_classI_for_train]
	indices_classJ_samples_train = indices_classJ_samples[:number_of_samples_classJ_for_train]
	
	number_of_samples_classI_for_valid = int(TR_TS_VA_SPLIT[1] * np.size(indices_classI_samples))
	number_of_samples_classJ_for_valid = int(TR_TS_VA_SPLIT[1] * np.size(indices_classJ_samples))

	start_vl_classI = number_of_samples_classI_for_train
	end_vl_classI = start_vl_classI + number_of_samples_classI_for_valid

	start_vl_classJ = number_of_samples_classJ_for_train
	end_vl_classJ = start_vl_classJ + number_of_samples_classJ_for_valid
	
	indices_classI_samples_valid = indices_classI_samples[start_vl_classI:end_vl_classI]
	indices_classJ_samples_valid = indices_classJ_samples[start_vl_classJ:end_vl_classJ]

	print "Total class %d samples %d "%(classI, np.size(indices_classI_samples))
	print "data split tr %d valid %d" %(number_of_samples_classI_for_train, \
	    number_of_samples_classI_for_valid)
	print "Total class %d samples %d "%(classJ, np.size(indices_classJ_samples))
	print "data split tr %d valid %d" %(number_of_samples_classJ_for_train, \
	    number_of_samples_classJ_for_valid)

	#Prepare train data for cc
	indices_input_samples_train = np.array([])
	indices_output_samples_train = np.array([])
		
	if classI != classJ:	
		for index_classI_sample in indices_classI_samples_train:
			indices_classI_samples_array = np.empty(indices_classJ_samples_train.size)
			indices_classI_samples_array.fill(index_classI_sample)
			indices_input_samples_train = np.concatenate((indices_input_samples_train, indices_classI_samples_array), axis = 0)
			indices_output_samples_train = np.concatenate((indices_output_samples_train, indices_classJ_samples_train), axis = 0)

		#Prepare validation data for cc
		indices_input_samples_valid = np.array([])
		indices_output_samples_valid = np.array([])
	
		for index_classI_sample in indices_classI_samples_valid:
			indices_classI_samples_array = np.empty(indices_classJ_samples_valid.size)
			indices_classI_samples_array.fill(index_classI_sample)
			indices_input_samples_valid = np.concatenate((indices_input_samples_valid, indices_classI_samples_array), axis = 0)
			indices_output_samples_valid = np.concatenate((indices_output_samples_valid, indices_classJ_samples_valid), axis = 0)

	else:
		indices_input_samples_train = indices_classI_samples_train		
		indices_output_samples_train = indices_classJ_samples_train	
		indices_input_samples_valid = indices_classI_samples_valid		
		indices_output_samples_valid = indices_classJ_samples_valid	

	print "Number of samples for CC train %d, for validation %d" %(np.size(indices_input_samples_train), np.size(indices_input_samples_valid))			
	#unit test	
	if (np.size(indices_input_samples_train) != np.size(indices_output_samples_train)):
		raise NameError('Input and output data dimensions are not matching for CC')

	obj_output_cc = output_cc()
	#permuted data
	obj_output_cc.input_train_perm = visual_features_dataset[indices_input_samples_train.astype(int), :]
	obj_output_cc.output_train_perm = visual_features_dataset[indices_output_samples_train.astype(int), :]
	obj_output_cc.input_valid_perm = visual_features_dataset[indices_input_samples_valid.astype(int), :]
	obj_output_cc.output_valid_perm = visual_features_dataset[indices_output_samples_valid.astype(int), :]
	#pdb.set_trace()
	#permuted indices
	obj_output_cc.indices_input_samples_train_perm = indices_input_samples_train
	obj_output_cc.indices_ouput_samples_train_perm = indices_output_samples_train
	obj_output_cc.indices_input_samples_valid_perm = indices_input_samples_valid
	obj_output_cc.indices_output_samples_valid_perm = indices_output_samples_valid
			
	return obj_output_cc

class input_data:
	dataset_name = []
	system_type = []
	train_class_labels = np.array([])
	test_class_labels = np.array([])
	visual_features_dataset = np.array([])
	attributes = np.array([])
	dataset_labels = np.array([])
	def function(self):
		print("This is the input_data class")	

def function_normalise_data(unnormalised_data):
	#Norimalise along each dimension separately
	norm_type = 2
	if norm_type == 1:	
		print "Normalisation between 0 to 1 ..."
		max_val_array = unnormalised_data.max(axis = 0)
		max_val_array[max_val_array == 0] = 1.
		max_val_mat = np.tile(max_val_array, (unnormalised_data.shape[0], 1))
		normalised_data = unnormalised_data/max_val_mat
		#Normalise entire data between [0,1]
		#if unnormalised_data.shape[0] != 0:
		#	if (unnormalised_data.max() != unnormalised_data.min()):
		#		normalised_data = np.divide((unnormalised_data - unnormalised_data.min()), (unnormalised_data.max() - unnormalised_data.min()))
		#	else:
		#		normalised_data = unnormalised_data * 0
		#else:
		#	normalised_data = []
		raise NameError("Something went wrong in normalisation...") 
	elif norm_type == 2:
		print "Normalisation between -1 to 1 ..."

		if unnormalised_data.shape[0] != 0:
			if (unnormalised_data.max() != unnormalised_data.min()):
				normalised_data = np.divide((unnormalised_data - unnormalised_data.min()), (unnormalised_data.max() - unnormalised_data.min()))
			else:
				normalised_data = unnormalised_data * 0
			normalised_data = normalised_data * 2 - 1
		else:
			normalised_data = []
			raise NameError("Something went wrong in normalisation...") 
		
	else:
		print "No normalisation ..."
		normalised_data = unnormalised_data
	return normalised_data

def function_get_input_data(obj_input_data):

	if obj_input_data.system_type == 'desktop':
		BASE_PATH = "/nfs4/omkar/Documents/"
	else:
		BASE_PATH = "/media/omkar/windows-D-drive/"
	print(BASE_PATH)
	if obj_input_data.dataset_name == 'apy':
		path_CNN_features = BASE_PATH + "/study/phd-research/data/code-data/semantic-similarity/cnn-features/aPY/cnn_feat_imagenet-vgg-verydeep-19.mat"
		path_attributes = BASE_PATH + "/study/phd-research/data/code-data/semantic-similarity/cnn-features/aPY/class_attributes.mat"
		features = scipy.io.loadmat(path_CNN_features)
		attributes_data = scipy.io.loadmat(path_attributes)
		attributes = attributes_data['class_attributes']
		dataset_labels = attributes_data['labels']
		visual_features_dataset = features['cnn_feat']
		visual_features_dataset = visual_features_dataset.transpose()
		train_class_labels = np.array([8, 12, 17, 23, 24])#, 8, 10, 11, 13, 15, 17, 21, 28, 29, 31])
		#train_class_labels = np.arange(1, 33, 1)
		test_class_labels = np.arange(21, 33, 1)
        
#'1 aeroplane' '2 bicycle''3 bird''4 boat''5 bottle''6 bus''7 car''8 cat''9 chair''10 cow''11 diningtable''12 dog''13 horse'
	    #'14 motorbike''15 person''16 pottedplant''17 sheep''18 sofa''19 train''20 tvmonitor''21 donkey''22 monkey''23 goat''24 wolf'
    	#'25 jetski''26 zebra''27 centaur''28 mug''29 statue''30 building''31 bag''32 carriage'
	else:
		tmp = scipy.io.loadmat('data/sample_dataset')
		dataset_labels = np.array(tmp['dataset_labels'])
		attributes = np.array(tmp['attributes'])
		visual_features_dataset = tmp['visual_features_dataset']
		train_class_labels = np.array([1, 2, 3])
		test_class_labels = np.array([1	, 2, 3])
	#pdb.set_trace()	
	obj_input_data.test_class_labels = test_class_labels 
	obj_input_data.train_class_labels = train_class_labels 
	obj_input_data.attributes = attributes 
	obj_input_data.visual_features_dataset = visual_features_dataset
	obj_input_data.dataset_labels = dataset_labels

	return obj_input_data

class classifier_data():
	train_data = []
	valid_data = []
	test_data = []
	train_labels = []	
	valid_labels = []	
	test_labels = []
	cross_features_train = np.array([])	
	cross_features_valid = np.array([])	
	cross_features_test = np.array([])	
	epochs = []
	number_of_train_classes = []
	dim_hidden_layer1 = []
		
	def function(self):
		print "This is a classifer data object..."


def function_reduce_dimension_of_data(visual_features_dataset_ori, REDUCED_DIMENSION): 
	
	print "Doing PCA to reduce dimension from %d to %d"%(visual_features_dataset_ori.shape[1], REDUCED_DIMENSION)
	#scale function scales the data to have zero mean and unit variance
	visual_features_dataset_norm = scale(visual_features_dataset_ori)
	visual_features_dataset_norm.mean(axis=0)
	visual_features_dataset_norm.std(axis=0)
	pca = PCA(n_components=REDUCED_DIMENSION)
	pca.fit(visual_features_dataset_norm)
	#The amount of variance that each PC explains (lambda_i/sum_i(lambda_i))
	var= pca.explained_variance_ratio_
	#Cumulative Variance explains
	var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
	if 0:
		plt.figure(1)
		plt.plot(var1)
		plt.ylabel('var1')
		plt.grid()
		plt.figure(2)
		plt.plot(var)
		plt.ylabel('var')
		plt.grid()
		plt.figure(3)
		plt.plot(visual_features_dataset_norm.mean(axis=0))
		plt.ylabel('visual_features_dataset_norm.mean')
		plt.grid()
		plt.figure(4)
		plt.plot(visual_features_dataset_norm.std(axis=0))
		plt.ylabel('visual_features_dataset_norm.std')
		plt.grid()
		pdb.set_trace()

	visual_features_dataset = pca.fit_transform(visual_features_dataset_norm)	

	if 0:
		plt.figure(5)
		plt.plot(visual_features_dataset.std(axis=0))
		plt.ylabel('visual_features_dataset_norm.std')
		plt.grid()
		plt.show()
        #visual_features_dataset_norm = StandardScaler().fit_transform(visual_features_dataset_ori)
	#visual_features_dataset = PCA(n_components = REDUCED_DIMENSION_VISUAL_FEATURE).fit_transform(visual_features_dataset_norm)
	#visual_features_dataset = function_normalise_data(visual_features_dataset)
	
	return visual_features_dataset

