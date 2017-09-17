# coding: UTF-8

from flask import Flask, render_template, request, redirect, jsonify, url_for
from models import *
import io
import csv
import pandas as pd
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.before_request
def before_request():
	initialize_db()

# after_requestはリクエストが成功した時のみ、処理されるけど、teardownはエラーでもなる
@app.teardown_request
def teardown_request(exception):
	db.close()



@app.route('/')
def index():
	return render_template(
		'index.html'
		, csv_files=Csv_file.select()
		)

	# csv_files = []
	# for csv_file in Csv_file.select():
	# 	csv_files.append({
	# 		'id': csv_file[0]
	# 		, 'name': csv_file[1]
	# 		, 'created+time': csv_file[2]
	# 		})
	# print csv_files
	# return render_template('index.html', csv_files='%s' % csv_files)


@app.route('/file/<id>')
def show_file(id):
	csv_file=Csv_file.get(Csv_file.id==id)
	return render_template(
		'file.html'
		, csv_file=csv_file
		, sales=csv_file.regi_sales
		)



@app.route('/upload', methods=['POST'])
def csv_save():
	csvfile = request.files.get('csvfile')
	if request.form['name'] == "":
		return (u'名前つけてください。あとからわかんなくなります。')
	elif 'text/csv' != csvfile.mimetype:
		return (u'CSVファイルを選択してください'), 415
	# elif len(pd.read_csv(csvfile, header=1, encoding='shift-jis').columns) != 10:
	# 	return (u'これって、Airレジバックオフィスからダウンロードした「売り上げ集計」のcsvですか？違いますよね？ダメです〜。')
	else:
		name=request.form['name']

		new_file = Csv_file.create(
						name=name
					)

		df = pd.read_csv(csvfile, skiprows=1, names=['businessday', 'sales_amount', 'check_num', 'sales_per_check', 'vistor_num', 'sales_amount_per_vis', 'order_num', 'payment_cash', 'payment_others', 'payment_discount'], encoding='shift-jis')
		for i, v in df.iterrows():
			print (i, v['businessday'], v['sales_amount'], v['check_num'], v['sales_per_check'], v['vistor_num'], v['sales_amount_per_vis'], v['order_num'], v['payment_cash'], v['payment_others'], v['payment_discount'])
			Regi_sale.create(
					csv_file_id=new_file.id
					, business_day=v['businessday']
					, sales_amount=v['sales_amount']
					, check_num=v['check_num']
					, sales_per_check=v['sales_per_check']
					, vistor_num=v['vistor_num']
					, sales_amount_per_vis=v['sales_amount_per_vis']
					, order_num=v['order_num']
					, payment_cash=v['payment_cash']
					, payment_others=v['payment_others']
					, payment_discount=v['payment_discount']
				)
		# return render_template('index.html', dataset='%s' %df)
		return redirect(url_for('index'))


if __name__=="__main__":
	app.run(debug=True)


