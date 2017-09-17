# coding: UTF-8

from flask import Flask, render_template, request, redirect, jsonify, url_for
import io
import csv
import pandas as pd
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')



	import io

from flask import Flask, jsonify, request





@app.route('/upload', methods=['POST'])
def csv_upload():
	filebuf = request.files.get('csvfile')
	if filebuf is None:
		return (u'ファイルを指定してください'), 400
	elif 'text/csv' != filebuf.mimetype:
		return (u'CSVファイル以外は受け付けません'), 415
	else:
		# dataset = pd.read_csv(filebuf, encoding='shift-jis')
		dataset = pd.read_csv(filebuf, error_bad_lines=False , header=None, encoding='shift-jis')
		print dataset

		return render_template('index.html', dataset='%s' %dataset, df='%s' %df)








if __name__=="__main__":
	app.run(debug=True)


