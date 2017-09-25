# coding: UTF-8

from flask import Flask, render_template, request, redirect, jsonify, url_for
from models import *
import io
import csv
import pandas as pd
import numpy as np
pd.options.display.notebook_repr_html = True

import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

# """Get data from MySQL with pandas library."""
import MySQLdb
import pandas.io.sql as psql


# グラフ書く
# import matplotlib
# import matplotlib.pyplot as plt
# チャートが綺麗になるおまじない設定
# plt.style.use('ggplot') 
# font = {'family' : 'meiryo'}
# matplotlib.rc('font', **font)



@app.before_request
def before_request():
	initialize_db()

# after_requestはリクエストが成功した時のみ、処理されるけど、teardownはエラーでもなる
@app.teardown_request
def teardown_request(exception):
	db.close()







@app.route('/')
def index():
	csv_files=Csv_file.select().order_by(Csv_file.created_time.desc())
	return render_template(
		'index.html'
		, csv_files=csv_files
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
	con = MySQLdb.connect(db='csv_db', user='root', passwd='root') # DB接続
	sql = 'SELECT * FROM regi_sale WHERE csv_file_id = %s' %id
	df = psql.read_sql(sql, con) # pandasのDataFrameの形でデータを取り出す
	con.close()
	dfsum=df.sum()
	dfmean=df.mean()
	sales_amount = dfsum.sales_amount
	check_num = dfsum.check_num
	sales_per_check = int(dfmean.sales_per_check)
	vistor_num = dfsum.vistor_num
	sales_amount_per_vis = int(dfmean.sales_amount_per_vis)
	order_num = dfsum.order_num
	payment_cash = dfsum.payment_cash
	payment_others = dfsum.payment_others
	payment_discount = dfsum.payment_discount

	csv_file=Csv_file.get(Csv_file.id==id)
	return render_template(
		'file.html'
		, csv_file=csv_file
		, sales=csv_file.regi_sales
		, sales_amount = sales_amount
		, check_num = check_num
		, sales_per_check = sales_per_check
		, vistor_num = vistor_num
		, sales_amount_per_vis = sales_amount_per_vis
		, order_num = order_num
		, payment_cash = payment_cash
		, payment_others = payment_others
		, payment_discount = payment_discount
		)



@app.route('/upload', methods=['POST'])
def csv_save():
	csvfile = request.files.get('csvfile')
	df = pd.read_csv(csvfile, skiprows=1, names=['businessday', 'sales_amount', 'check_num', 'sales_per_check', 'vistor_num', 'sales_amount_per_vis', 'order_num', 'payment_cash', 'payment_others', 'payment_discount'], encoding='shift-jis')
	if request.form['name'] == "":
		return (u'名前つけてください。あとからわかんなくなります。')
	elif 'text/csv' != csvfile.mimetype:
		return (u'CSVファイルを選択してください'), 415
	elif df['businessday'].isnull().any() == True or df['sales_amount'].isnull().any() == True or df['check_num'].isnull().any() == True or df['sales_per_check'].isnull().any() == True or df['vistor_num'].isnull().any() == True or df['sales_amount_per_vis'].isnull().any() == True or df['order_num'].isnull().any() == True or df['payment_cash'].isnull().any() == True or df['payment_others'].isnull().any() == True or df['payment_discount'].isnull().any() == True:
		return (u'これって、Airレジバックオフィスからダウンロードした「売り上げ集計」のcsvですか？違いますよね？ダメです〜。')
	# elif: 文字タイプのチェックをここに入れる
	else:
		name=request.form['name']

		new_file = Csv_file.create(
						name=name
					)
		for i, v in df.iterrows():
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
		return redirect(url_for('index'))


if __name__=="__main__":
	app.run(debug=True)


