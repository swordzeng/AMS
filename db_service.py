import sqlite3
import pandas as pd

DB_PATH = 'AMS.db'

def table_append(df, table):
	conn = sqlite3.connect(DB_PATH)
	df.to_sql(table, con=conn, if_exists='append', index=False)
	conn.close()

def get_latest_date(table, column, value):
	conn = sqlite3.connect(DB_PATH)
	query = "SELECT MAX(Date) AS Max_Date FROM {} WHERE {} = '{}'".format(table, column, value)
	df_max_date = pd.read_sql(query, con=conn)
	conn.close()

	max_date = '2019-12-01' if df_max_date.iat[0,0] == None else  df_max_date.iat[0,0]

	return max_date