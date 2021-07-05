import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler

# Fixed parameters
N_SIGNALS = 3
N_SIGNALS_GRANULAR = 7
N_FEATURES = 25
# Tunable Hyperparameters
DROPOUT = None
LEARNING_RATE = None
LEARNING_RATE_DECAY = None
# Model
MODEL = None 
DEVICE = None
CRITERION = None
OPTIMIZER = None
SCHEDULER = None

#
# ---------- MODELS TRAINED ON RASPBERRY PI ----------
#
class CryptoSoothsayer_Pi_0(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_0, self).__init__()
		self.layer_1 = nn.Linear(input_size, 5)
		self.layer_output = nn.Linear(5, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_0"



class CryptoSoothsayer_Pi_1(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_1, self).__init__()
		self.layer_1 = nn.Linear(input_size, 6)
		self.layer_output = nn.Linear(6, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_1"



class CryptoSoothsayer_Pi_2(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_2, self).__init__()
		self.layer_1 = nn.Linear(input_size, 7)
		self.layer_output = nn.Linear(7, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_2"



class CryptoSoothsayer_Pi_3(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_3, self).__init__()
		self.layer_1 = nn.Linear(input_size, 8)
		self.layer_output = nn.Linear(8, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_3"



class CryptoSoothsayer_Pi_4(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_4, self).__init__()
		self.layer_1 = nn.Linear(input_size, 9)
		self.layer_output = nn.Linear(9, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_4"



class CryptoSoothsayer_Pi_5(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_5, self).__init__()
		self.layer_1 = nn.Linear(input_size, 10)
		self.layer_output = nn.Linear(10, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_5"



class CryptoSoothsayer_Pi_6(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_6, self).__init__()
		self.layer_1 = nn.Linear(input_size, 11)
		self.layer_output = nn.Linear(11, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_6"



class CryptoSoothsayer_Pi_7(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Pi_7, self).__init__()
		self.layer_1 = nn.Linear(input_size, 12)
		self.layer_output = nn.Linear(12, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Pi_7"



#
# ---------- MODELS TRAINED ON OLD PC ----------
#
class CryptoSoothsayer_PC_0(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_0, self).__init__()
		self.layer_1 = nn.Linear(input_size, 13)
		self.layer_output = nn.Linear(13, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_0"



class CryptoSoothsayer_PC_1(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_1, self).__init__()
		self.layer_1 = nn.Linear(input_size, 14)
		self.layer_output = nn.Linear(14, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_1"



<<<<<<< HEAD
class CryptoSoothsayer_PC_3(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_3, self).__init__()
		self.layer_1 = nn.Linear(input_size, 78125)
		self.layer_2 = nn.Linear(78125, 3125)
		self.layer_3 = nn.Linear(3125, 125)
		self.layer_output = nn.Linear(125, n_signals)
=======
class CryptoSoothsayer_PC_2(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_2, self).__init__()
		self.layer_1 = nn.Linear(input_size, 15)
		self.layer_output = nn.Linear(15, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_2"



class CryptoSoothsayer_PC_3(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_3, self).__init__()
		self.layer_1 = nn.Linear(input_size, 16)
		self.layer_output = nn.Linear(16, n_signals)
>>>>>>> 103032e1dbb9bcabdbb84302c9c8f5ccd49be863
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
<<<<<<< HEAD
		out = self.dropout(F.relu(self.layer_2(out)))
		out = self.dropout(F.relu(self.layer_3(out)))
=======
>>>>>>> 103032e1dbb9bcabdbb84302c9c8f5ccd49be863
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_3"



class CryptoSoothsayer_PC_4(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_4, self).__init__()
<<<<<<< HEAD
		self.layer_1 = nn.Linear(input_size,13 )
		self.layer_output = nn.Linear(13, n_signals)
=======
		self.layer_1 = nn.Linear(input_size, 17)
		self.layer_output = nn.Linear(17, n_signals)
>>>>>>> 103032e1dbb9bcabdbb84302c9c8f5ccd49be863
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_4"

<<<<<<< HEAD
=======


class CryptoSoothsayer_PC_5(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_5, self).__init__()
		self.layer_1 = nn.Linear(input_size, 18)
		self.layer_output = nn.Linear(18, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_5"



class CryptoSoothsayer_PC_6(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_PC_6, self).__init__()
		self.layer_1 = nn.Linear(input_size, 19)
		self.layer_output = nn.Linear(19, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_PC_6"


>>>>>>> 103032e1dbb9bcabdbb84302c9c8f5ccd49be863

#
# ---------- MODELS TRAINED ON LAPTOP ----------
#
class CryptoSoothsayer_Laptop_0(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_0, self).__init__()
		self.layer_1 = nn.Linear(input_size, 20)
		self.layer_output = nn.Linear(20, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_0"



class CryptoSoothsayer_Laptop_1(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_1, self).__init__()
		self.layer_1 = nn.Linear(input_size, 21)
		self.layer_output = nn.Linear(21, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_1"



class CryptoSoothsayer_Laptop_2(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_2, self).__init__()
		self.layer_1 = nn.Linear(input_size, 22)
		self.layer_output = nn.Linear(22, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_2"



class CryptoSoothsayer_Laptop_3(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_3, self).__init__()
		self.layer_1 = nn.Linear(input_size, 23)
		self.layer_output = nn.Linear(23, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out


	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_3"



class CryptoSoothsayer_Laptop_4(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_4, self).__init__()
		self.layer_1 = nn.Linear(input_size, 24)
		self.layer_output = nn.Linear(24, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_4"



class CryptoSoothsayer_Laptop_5(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_5, self).__init__()
		self.layer_1 = nn.Linear(input_size, 20)
		self.layer_2 = nn.Linear(20, 13)
		self.layer_output = nn.Linear(13, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.dropout(F.relu(self.layer_2(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_5"



class CryptoSoothsayer_Laptop_6(nn.Module):
	def __init__(self, input_size, n_signals):
		super(CryptoSoothsayer_Laptop_6, self).__init__()
		self.layer_1 = nn.Linear(input_size, 21)
		self.layer_2 = nn.Linear(21, 13)
		self.layer_output = nn.Linear(13, n_signals)
		self.dropout = nn.Dropout(DROPOUT)


	def forward(self, inputs):
		out = self.dropout(F.relu(self.layer_1(inputs)))
		out = self.dropout(F.relu(self.layer_2(inputs)))
		out = self.layer_output(out)
		return out

	
	def get_class_name(self):
		return "CryptoSoothsayer_Laptop_6"


#
# -------------- GETTERS & SETTERS ---------------
#

def set_model_props(model):
	global DEVICE, CRITERION, OPTIMIZER, SCHEDULER

	DEVICE = torch.device("cpu")
	model.to(DEVICE)
	CRITERION = nn.CrossEntropyLoss()
	OPTIMIZER = optim.Adam(model.parameters(), lr=LEARNING_RATE)
	lambda1 = lambda epoch: LEARNING_RATE_DECAY 
	SCHEDULER =  lr_scheduler.MultiplicativeLR(OPTIMIZER, lambda1)



def set_model(model_architecture): 
	global MODEL

	if "Laptop_0" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_0(N_FEATURES, N_SIGNALS)
	elif "Laptop_1" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_1(N_FEATURES, N_SIGNALS)
	elif "Laptop_2" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_2(N_FEATURES, N_SIGNALS)
	elif "Laptop_3" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_3(N_FEATURES, N_SIGNALS)
	elif "Laptop_4" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_4(N_FEATURES, N_SIGNALS)
	elif "Laptop_5" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_5(N_FEATURES, N_SIGNALS)
	elif "Laptop_6" in model_architecture:
		MODEL = CryptoSoothsayer_Laptop_6(N_FEATURES, N_SIGNALS)
	elif "Pi_0" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_0(N_FEATURES, N_SIGNALS)
	elif "Pi_1" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_1(N_FEATURES, N_SIGNALS)
	elif "Pi_2" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_2(N_FEATURES, N_SIGNALS)
	elif "Pi_3" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_3(N_FEATURES, N_SIGNALS)
	elif "Pi_4" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_4(N_FEATURES, N_SIGNALS)
	elif "Pi_5" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_5(N_FEATURES, N_SIGNALS)
	elif "Pi_6" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_6(N_FEATURES, N_SIGNALS)
	elif "Pi_7" in model_architecture:
		MODEL = CryptoSoothsayer_Pi_7(N_FEATURES, N_SIGNALS)
	elif "PC_0" in model_architecture:
		MODEL = CryptoSoothsayer_PC_0(N_FEATURES, N_SIGNALS)
	elif "PC_1" in model_architecture:
<<<<<<< HEAD
		MODEL = CryptoSoothsayer_PC_1(N_FEATURES, N_SIGNALS_GRANULAR)
	elif "PC_3" in model_architecture:
		MODEL = CryptoSoothsayer_PC_3(N_FEATURES, N_SIGNALS_GRANULAR)
	elif "PC_4" in model_architecture:
		MODEL = CryptoSoothsayer_PC_4(N_FEATURES, N_SIGNALS_GRANULAR)
=======
		MODEL = CryptoSoothsayer_PC_1(N_FEATURES, N_SIGNALS)
	elif "PC_2" in model_architecture:
		MODEL = CryptoSoothsayer_PC_2(N_FEATURES, N_SIGNALS)
	elif "PC_3" in model_architecture:
		MODEL = CryptoSoothsayer_PC_3(N_FEATURES, N_SIGNALS)
	elif "PC_4" in model_architecture:
		MODEL = CryptoSoothsayer_PC_4(N_FEATURES, N_SIGNALS)
	elif "PC_5" in model_architecture:
		MODEL = CryptoSoothsayer_PC_5(N_FEATURES, N_SIGNALS)
	elif "PC_6" in model_architecture:
		MODEL = CryptoSoothsayer_PC_6(N_FEATURES, N_SIGNALS)
>>>>>>> 103032e1dbb9bcabdbb84302c9c8f5ccd49be863



def set_model_parameters(dropout=0, eta=0, eta_decay=0):
	global DROPOUT, LEARNING_RATE, LEARNING_RATE_DECAY

	DROPOUT = dropout
	LEARNING_RATE = eta
	LEARNING_RATE_DECAY = eta_decay



def set_pretrained_model(model):
	global MODEL
	MODEL = model



def get_model():
	global MODEL
	return MODEL



def get_model_parameters():
	global DROPOUT, LEARNING_RATE, LEARNING_RATE_DECAY
	return DROPOUT, LEARNING_RATE, LEARNING_RATE_DECAY



def get_device():
	global DEVICE
	return DEVICE

def get_criterion():
	global CRITERION
	return CRITERION

def get_optimizer():
	global OPTIMIZER
	return OPTIMIZER

def get_scheduler():
	global SCHEDULER
	return SCHEDULER

