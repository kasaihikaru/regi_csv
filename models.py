from peewee import *
import datetime

db = MySQLDatabase(
	'csv_db'
	, user='root'
	, passwd='root'
	, use_unicode=True
	, charset="utf8"
	, host="127.0.0.1"
	, port=3306
	)


class Csv_file(Model):
	id = PrimaryKeyField()
	name = CharField()
	created_time = DateTimeField(default = datetime.datetime.now)

	class Meta:
		database = db


class Regi_sale(Model):
	id = PrimaryKeyField()
	csv_file = ForeignKeyField(Csv_file, related_name='regi_sales')	
	created_time = DateTimeField(default = datetime.datetime.now)
	business_day = IntegerField()
	sales_amount = IntegerField()
	check_num = IntegerField()
	sales_per_check = IntegerField()
	vistor_num = IntegerField()
	sales_amount_per_vis = IntegerField()
	order_num = IntegerField()
	payment_cash = IntegerField()
	payment_others = IntegerField()
	payment_discount = IntegerField()

	class Meta:
		database = db



def initialize_db():
	db.connect()
	db.create_table(Csv_file, safe=True)
	db.create_table(Regi_sale, safe=True)

	