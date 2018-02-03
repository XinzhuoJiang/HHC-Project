import pandas as pd 
from datetime import datetime
from datetime import timedelta
import numpy as np 
import pickle

patient_data = pd.read_csv('S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Train_Test_Data/app_numofvisit_greaterthan0_test.csv')
Practice_Noshow_df = pd.read_csv('S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Static_Data/Practice_Noshow_df.csv', header = None)
Dept_Number_df = pd.read_csv('S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Static_Data/Dept_number.csv')
Hour_Noshow_df = pd.read_csv('S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Static_Data/Hour_Noshow_df.csv', header = None)
Month_Noshow_df = pd.read_csv('S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Static_Data/Month_Noshow_df.csv', header = None)

Practice_Noshow_df = Practice_Noshow_df.set_index(0)
Dept_Number_df = Dept_Number_df.drop(['Unnamed: 0'], axis = 1)

patient_data['MRN'] = (patient_data['MRN']).astype(int)
patient_info = patient_data.drop(['Unnamed: 0','NoShowInd'], axis = 1)

patient_info_simple = patient_info.groupby('MRN').last().reset_index()

def no_show_func(MRN, dept, start_time, practice, pred_method):
	patient_MRN = int(MRN)
	patient_dept = dept.upper()
	patient_practice = practice

	patient_sched_info = pd.DataFrame(patient_info_simple.loc[patient_info_simple['MRN'] == patient_MRN])
	patient_sched_info['Dept'] = Dept_Number_df.loc[Dept_Number_df['Name'] == patient_dept, 'number'].iloc[0]
	patient_sched_info['Practice'] = patient_practice
	patient_sched_info['Practice1'] = Practice_Noshow_df.loc[practice][1]
	patient_sched_info = patient_sched_info.drop(['MRN','Practice','Poverty'], axis = 1)

	i = patient_sched_info.index[0]
#Time
	start_time = pd.to_datetime(start_time)
	date_time_slot = [start_time]
	S = 9
	T = 9
	for i in range(1, T):
	    if (start_time - timedelta(days = i)).weekday() == 6:
	        T += 1
	    else:
	        time_ori = start_time - timedelta(days = i)
	        date_time_slot.append(time_ori)

	for j in range(1, S):
	    if (start_time + timedelta(days = j)).weekday() == 6:
	        S += 1
	    else:
	        time_end = start_time + timedelta(days = j)
	        date_time_slot.append(time_end)

	hour1 = []
	for i in range(7, 20):
	    hour1.append(i)
	hour = list(Hour_Noshow_df[1][2:])
	strftime_ls = [x.strftime('%Y-%m-%d') for x in date_time_slot]
	
#load method
	predict_matrix = []
	for i in date_time_slot:
	    for j in hour:
	        patient_sched_info['month1'] = Month_Noshow_df.loc[Month_Noshow_df[0] == i.month, 1].iloc[0]
	        patient_sched_info['weekday'] = i.weekday()
	        patient_sched_info['Leaddays'] = (i - datetime.now()).days
	        patient_sched_info['hour1'] = j
	        predict = pred_method.predict_proba(patient_sched_info)[:,1][0]
	        predict_matrix.append(predict)

	predict_matrix = np.array(predict_matrix)
	predict_matrix = predict_matrix.reshape(len(date_time_slot), 13)
	df = pd.DataFrame(predict_matrix, columns = hour1, index = strftime_ls)
	return df

def sav_load(file_path):
	file = open(file_path, 'rb')
	pred_method_load = pickle.load(file, encoding = 'latin1')
	return pred_method_load

#logit_file_path = 'S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Machine_Learning_Method_Data/L1_model.sav'
#pred_method_logit = sav_load(logit_file_path)


#RF_file_path = 'S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Machine_Learning_Method_Data/RF_model.sav'
#pred_method_logit = sav_load(RF_file_path)

#decision_file_path = 'S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Machine_Learning_Method_Data/decision_model.sav'
#pred_method_decision = sav_load(decision_file_path)

#NN_file_path = 'S:/ExecutiveAdministration/Health Analytics/Internship Program/4. Appointment Show Rate/Logistic Regression/Data/Machine_Learning_Method_Data/NN_model.sav'
#pred_method_NN = sav_load(NN_file_path)

#logit_predict_result = no_show_func(MRN, dept, start_time, parctice, pred_method_logit, patient_info_simple)
#RF_predict_result = no_show_func(MRN, dept, start_time, parctice, logit_file_path, patient_info_simple)
#decision_predict_result = no_show_func(MRN, dept, start_time, parctice, decision_file_path, patient_info_simple)
#NN_predict_result = no_show_func(MRN, dept, start_time, parctice, NN_file_path, patient_info_simple)

#four_model_result = pd.DataFrame(logit_predict_result + RF_predict_result + NN_predict_result + decision_predict_result)