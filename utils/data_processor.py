import os
import pandas as pd
import torch
from datetime import datetime
import time
import random
import numpy as np
import neural_nets as nn
'''
WHEN testing need this version instead
'''
#from utils import neural_nets as nn

BATCH_SIZE = 256 
EPOCHS = 1
COIN = "bitcoin"
REPORTS = []

#
# ------------ DATA RELATED -----------
#
def shuffle_data(data):
	'''
	Used for shuffling the data during the training/validation phases.
	'''
	size = len(data)
	for row_ind in range(size):
		swap_row_ind = random.randrange(size)
		tmp_row = data[swap_row_ind]
		data[swap_row_ind] = data[row_ind]
		data[row_ind] = tmp_row

	return data



def generate_dataset(data, limit, offset, data_aug_per_sample=0):
	'''
	Returns a list of tuples, of which the first element of the tuple is the list of values for the features and the second is the target value
	NOTES: 
		- data_aug_per_sample param determines how many extra datapoints to generate per each original datapoint * its frequency metric (i.e., signal_ratios)
		- signal_ratios variable is used to upsample underrepresented categories more than their counterparts when augmenting the data
	'''
	# to determine relative frequency of signals
	new_data = data.iloc[:limit,:]
	vals = new_data["signal"].value_counts().sort_index()
	signal_ratios = [vals.max()/x for x in vals]

	dataset = []
	for row in range(offset, limit):
		target = data.iloc[row, -1]
		row_features = []

		for feature in range(nn.N_FEATURES):
			row_features.append(data.iloc[row, feature])
		datapoint_tuple = (row_features, target)
		dataset.append(datapoint_tuple)

		# this evens out the datapoints per category
		for i in range(data_aug_per_sample * round(signal_ratios[target])):
			row_features_aug = []
			for feature in range(nn.N_FEATURES):
				rand_factor = 1 + random.uniform(-0.00001, 0.00001)
				row_features_aug.append(data.iloc[row, feature] * rand_factor)
			datapoint_tuple_aug = (row_features_aug, target)
			dataset.append(datapoint_tuple_aug)

	return dataset


def get_datasets(coin, data_aug_factor=0):
	'''
	Splits dataset into training, validation, and testing datasets.
	NOTE: uses no data augmentation by default and will only apply data_aug_factor to the training dataset.
	'''
	global REPORTS

	# Load data
	data = pd.read_csv(f"datasets/complete/{coin}_historical_data_complete.csv")
	data = data.drop(columns=["date"])
	data["signal"] = data["signal"].astype("int64")

	# Split into training, validation, testing
	# 70-15-15 split
	n_datapoints = data.shape[0]
	train_end = int(round(n_datapoints*0.7))
	valid_end = train_end + int(round(n_datapoints*0.15))


	train_data = generate_dataset(data, train_end, 0, data_aug_factor)
	REPORTS.append(f"Length Training Data: {len(train_data)}")

	valid_data = generate_dataset(data, valid_end, train_end)
	REPORTS.append(f"Length Validation Data: {len(valid_data)}")

	test_data = generate_dataset(data, n_datapoints, valid_end)
	REPORTS.append(f"Length Testing Data: {len(test_data)}") 

	return train_data, valid_data, test_data


#
# ------------ SAVING/LOADING FUNCTIONS -----------
#
# save model
def save_model(model, filepath):
	torch.save(model.state_dict(), filepath)


# load model
def load_model(neural_net, filepath):
	model = neural_net
	model.load_state_dict(torch.load(filepath))

	return model


#
# ----------- TRAINING FUNCTIONS ----------
#
def convert_to_tensor(feature, target):
	'''
	Converts the feature vector and target into pytorch-compatible tensors.
	'''
	feature_tensor = torch.tensor([feature], dtype=torch.float32)
	feature_tensor = feature_tensor.to(nn.get_device())
	target_tensor = torch.tensor([target], dtype=torch.int64)
	target_tensor = target_tensor.to(nn.get_device())

	return feature_tensor, target_tensor



def take_one_step(model, feature, target, train_loss):
	'''
	Forward propogates a single feature vector through the network, the back propogates based on the loss.
	Returns the cumulative training loss.
	'''
	# set to train mode here to activate components like dropout
	model.train()
	# make data pytorch compatible
	feature_tensor, target_tensor = convert_to_tensor(feature, target)
	# Forward
	model_output = model(feature_tensor)
	loss = nn.get_criterion()(model_output, target_tensor)
	# Backward
	nn.get_optimizer().zero_grad()
	loss.backward()
	nn.get_optimizer().step()
	# adjust learning rate
	nn.get_scheduler().step()
	train_loss += loss.item()

	return train_loss



def validate_model(model, valid_data, train_loss, min_valid_loss):
	'''
	Validates the model on the validation dataset.
	Returns the mininum validation loss, which could change depending on validation results.
	'''
	global REPORTS

	# set to evaluate mode to turn off components like dropout
	model.eval()
	valid_loss = 0.0
	for feature, target in valid_data:
		# make data pytorch compatible
		feature_tensor, target_tensor = convert_to_tensor(feature, target)
		# model makes prediction
		with torch.no_grad():
			model_output = model(feature_tensor)
			loss = nn.get_criterion()(model_output, target_tensor)
			valid_loss += loss.item()

	if valid_loss/len(valid_data) < min_valid_loss:
		min_valid_loss = valid_loss/len(valid_data)
		report = f"Training Loss: {train_loss:.4f} | Validation Loss: {min_valid_loss:.4f} | eta: {nn.OPTIMIZER.state_dict()['param_groups'][0]['lr']:.6f}"
		REPORTS.append(report)

	return min_valid_loss



def train(model, train_data, valid_data, start_time):
	global REPORTS, EPOCHS, BATCH_SIZE

	min_valid_loss = np.inf 
	
	train_data = shuffle_data(train_data)

	for epoch in range(EPOCHS):
		steps = 0
		train_loss = 0.0

		for feature, target in train_data:
			steps += 1
			# train model on feature
			train_loss = take_one_step(model, feature, target, train_loss)
			# if end of batch or end of dataset, validate model
			if steps % BATCH_SIZE == 0 or steps == len(train_data)-1:
				min_valid_loss = validate_model(model, valid_data, train_loss/steps, min_valid_loss)
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				print(f"System Time: {current_time} | Time Elapsed: {(time.time() - start_time) / 60:.1f} mins. | Training Loss: {train_loss/steps:.4f} | Min Validation Loss: {min_valid_loss:.4f}")

		report = f"Time elapsed by epoch {epoch+1}: {round((time.time() - start_time)) / 60} mins."
		REPORTS.append(report)
		print(report)



def evaluate_model(model, test_data):
	global REPORTS

	model.eval()
	correct = 0
	mostly_correct = 0
	safe_fail = 0
	nasty_fail = 0
	catastrophic_fail = 0
	for feature, target in test_data:
		feature_tensor, target_tensor = convert_to_tensor(feature, target)

		with torch.no_grad():
			output = model(feature_tensor)

		decision = torch.argmax(output, dim=1)

		# flawless
		if decision == target_tensor:
			correct += 1
		# correct direction, but extent was wrong (e.g., target = BUY X, decision = BUY 2X)
		elif (target_tensor == 0 or target_tensor == 1) and (decision == 0 or decision == 1):
			mostly_correct += 1
		# correct direction, but extent was wrong (e.g., target = SELL X, decision = SELL 2X)
		elif (target_tensor == 3 or target_tensor == 4) and (decision == 3 or decision == 4):
			mostly_correct += 1
		# catastrophic failure (e.g., told to buy when should have sold)
		elif (target_tensor > 2 and decision < 2) or (target_tensor < 2 and decision > 2):
			catastrophic_fail += 1
		# severe failure (e.g., should have hodled but was told to buy or sell
		elif target_tensor == 2 and (decision < 2 or decision > 2):
			nasty_fail += 1
		# decision was to hodl, but should have sold or bought
		else:
			safe_fail += 1

	report = f"""
	POSITIVE:
		[++] Perfect accuracy: {correct/len(test_data):>10.4f}
		[+] Model good enough accuracy: {(mostly_correct + correct)/len(test_data):>10.4f}
	NEGATIVE:
		[-] Told to hodl but should have sold/bought rate: {safe_fail/len(test_data):>10.4f}
		[--] Should have hodled but told to sell/buy rate: {nasty_fail/len(test_data):>10.4f}
		[---] Told to do the opposite of correct move rate: {catastrophic_fail/len(test_data):>10.4f}
		"""
	REPORTS.append(report)
	print(report)

	return [correct/len(test_data), (mostly_correct+correct)/len(test_data), nasty_fail/len(test_data), catastrophic_fail/len(test_data)]



#
# ---------- REPORTING FUNCTIONS ----------
#
def join_all_reports():
	global REPORTS

	final_report = ""
	for report in REPORTS:
		final_report += report + "\n"
	return final_report



def generate_report():
	report = open(f"reports/{nn.get_model().get_class_name()}_report.txt", "w")
	report.write(join_all_reports())
	report.close()



#
# ------------- Find the Most Promising Models -----------------
#
def validate_model_param_tuning(model, valid_data, min_valid_loss, model_architecture, model_counter):
	# set to evaluate mode to turn off components like dropout
	model.eval()
	valid_loss = 0.0
	for feature, target in valid_data:
		# make data pytorch compatible
		feature_tensor, target_tensor = convert_to_tensor(feature, target)
		# model makes prediction
		with torch.no_grad():
			model_output = model(feature_tensor)
			loss = nn.get_criterion()(model_output, target_tensor)
			valid_loss += loss.item()

	if valid_loss/len(valid_data) < min_valid_loss:
		min_valid_loss = valid_loss/len(valid_data)

	return min_valid_loss



def terminate_early(train_loss_comp_ind, train_loss, steps, last_train_loss):
	if train_loss_comp_ind >= 5 and ((train_loss/steps) - last_train_loss[train_loss_comp_ind-5]) > 0.001:
		print(f"5-Batch Diff: {(train_loss/steps) - last_train_loss[train_loss_comp_ind-5]}")
		return True
	if train_loss_comp_ind >= 10 and ((train_loss/steps) - last_train_loss[train_loss_comp_ind-10]) > 0:
		print(f"10-Batch Diff: {(train_loss/steps) - last_train_loss[train_loss_comp_ind-10]}")
		return True
	if train_loss_comp_ind >= 15 and ((train_loss/steps) - last_train_loss[train_loss_comp_ind-15]) > -0.1:
		print(f"15-Batch Diff: {(train_loss/steps) - last_train_loss[train_loss_comp_ind-15]}")
		return True
	
	return False



def parameter_tuner():
	global COIN, BATCH_SIZE, EPOCHS

	train_data, valid_data, test_data = get_datasets(COIN)
	model_counter = 0

	for eta in np.arange(0.001, 0.002, 0.0005):
		for decay in np.arange(0.9999, 0.99999, 0.00001):	
			for dropout in np.arange(0.05, 0.85, 0.05):
				print("Start of new Experiment\n__________________________")
				print(f"Eta: {eta} | Decay: {decay} | Dropout: {dropout}")
				report = "" 
				
				model_architecture = "Laptop_0"
				nn.set_model_parameters(dropout, eta, decay)
				nn.set_model(model_architecture) 
				nn.set_model_props(nn.get_model())
				model = nn.get_model()

				start_time = time.time()
				# Train
				min_valid_loss = np.inf 
				last_train_loss = [np.inf]
				train_loss_comp_ind = 0
				train_data = shuffle_data(train_data)

				for epoch in range(EPOCHS):
					steps = 0
					train_loss = 0.0

					for feature, target in train_data:
						steps += 1
						# train model on feature
						train_loss = take_one_step(model, feature, target, train_loss)
						# if end of batch or end of dataset, validate model
						if steps % BATCH_SIZE == 0 or steps == len(train_data)-1:
							min_valid_loss = validate_model_param_tuning(model, valid_data, min_valid_loss, model_architecture, model_counter)

							now = datetime.now()
							current_time = now.strftime("%H:%M:%S")
							print(f"System Time: {current_time} | Time Elapsed: {(time.time() - start_time) / 60:.1f} mins. | Training Loss: {train_loss/steps:.4f} | Min Validation Loss: {min_valid_loss:.4f}")
							# breaks if training loss increase exceeds threshhold (i.e., the model stops learning)
							last_train_loss.append(train_loss/steps)
							train_loss_comp_ind += 1
							if terminate_early(train_loss_comp_ind, train_loss, steps, last_train_loss):
								break


				save_model(model, f"models/CS_{model_architecture}_{model_counter}_mod.pt")
				
				mod_acc = evaluate_model(model, test_data)
				
				report += f"MODEL: {model_counter}\nTraining Loss: {last_train_loss[-1]} | Min Valid Loss: {min_valid_loss}\nPARAMETERS:\n\t{model_architecture}\n\teta: {nn.LEARNING_RATE} | decay: {nn.LEARNING_RATE_DECAY} | dropout: {nn.DROPOUT}\nDECISIONS:\n\tPerfect Decision: {mod_acc[0]}\n\tAcceptable Decision: {mod_acc[1]}\n\tSignal Should Have Been Hodl: {mod_acc[2]}\n\tSignal and Answer Exact Opposite: {mod_acc[3]}"
				
				if len(report) > 0:
					with open(f"reports/Parameter_Tuning_Report.txt", "a") as f:
					# starting from index 1 to avoid first triple space divider
						f.write(report + "\n\n")

					print("Report written")

				model_counter += 1

parameter_tuner()



#
# -------------- Continue Training Most Successful Experiments --------------
#
def continue_training():
	global REPORTS, COIN, EPOCHS, BATCH_SIZE
	# 
	# ------------ DATA GENERATION ----------
	#
	train_data, valid_data, test_data = get_datasets(COIN, 16)

	#
	# ------------ MODEL TRAINING -----------
	#
	model_architecture = "Laptop_0"
	model_number = 67
	model_filepath = f"models/CS_{model_architecture}_{model_number}_dummy.pt"
	
	nn.set_model_parameters(dropout = 0.2, eta = 0.001, eta_decay = 0.99994)
	nn.set_pretrained_model(load_model(nn.CryptoSoothsayer_Laptop_0(nn.N_FEATURES, nn.N_SIGNALS), model_filepath))
	nn.set_model_props()
	model = nn.get_model()

	dropout, eta, eta_decay = nn.get_model_parameters()
	reports = [f"Model: {model.get_class_name()}", f"Learning rate: {eta}", f"Learning rate decay: {eta_decay}", f"Chance of dropout: {dropout}", f"Batch size: {BATCH_SIZE}", f"Epochs: {EPOCHS}", f"Coin: {COIN}"]

	start_time = time.time()
	
	train(model, train_data, valid_data, start_time)
	save(model, file_path)

	#
	# ------------ MODEL TESTING -----------
	#
	# Load
	model = load_model(nn.get_model(), model_filepath)
	report = "EVALUATE TRAINED MODEL"
	REPORTS.append(report)
	print(report)
	evaluate_model(model, test_data)

	#
	# ---------- GENERATE REPORT -----------
	#
	generate_report()
	


#continue_training()
