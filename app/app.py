from flask import *
import json
import pandas as pd 
from noshow import no_show_func
from noshow import sav_load



# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')


@app.route('/search', methods=['GET'])
def render_home_page():
	return render_template('index.html')


@app.route('/search/info/api', methods=['POST'])

def get_info():
	obj = request.get_json(force=True)
	print(obj)
	MRN = obj['MRN']
	year = obj['year']
	month = obj['month']
	day = obj['day']
	hour = obj['hour']
	minute = obj['minute']
	dept = obj['Dept']
	practice = obj['Practice']
	start_time = str(year)+"-"+str(month)+"-"+str(day)+ " " + str(hour) + ":" + str(minute)
	logit_file_path = './Data/L1_model.sav'
	pred_method_logit = sav_load(logit_file_path)
	logit_predict_result = no_show_func(MRN, dept, start_time, practice, pred_method_logit)
	jsonfiles = logit_predict_result.to_json(orient='index')
	return jsonfiles     

if __name__ == "__main__":
	app.run()