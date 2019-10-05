from mysql import connector


class DatabaseUtils: 
	def __init__(self, database, table_name):
		self.db = database
		self.table_name = table_name
		self.conn = connector.connect(user = 'root',
									password = '1234',
									host = '127.0.0.1')
		self.cursor = self.conn.cursor()
		self.connect_to_db()
		self.create_table()

		
	def connect_to_db(self):
		try:
			self.conn.database = self.db
		except connector.Error as err:
			if err.errno == connector.errorcode.ER_BAD_DB_ERROR:
				self.create_db()
				self.conn.database = self.db
			else:
				print(err.msg)


	def create_db(self):
		try:
			self.run_command(f"CREATE  DATABASE {self.db};")
		except connector.Error as err:
			print(f"Error in create_db: {err}")


	def create_table(self):
		create_cmd = (
				f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
				"ID INT NOT NULL AUTO_INCREMENT,"
				"name VARCHAR(250) NOT NULL,"
				"price DECIMAL(15,2),"
				"link TEXT,"
				"description TEXT,"
				"PRIMARY KEY (id) );"
		)
		self.run_command(create_cmd)

		insert_cmd = (
				f"INSERT INTO {self.table_name} (name, price, description, link ) "
				"SELECT * FROM (SELECT 'job', 100.00, 'very cool company', 'http://vistamed.ru/') AS tmp "
				"WHERE NOT EXISTS (SELECT * FROM wish_list);"
		)
		self.run_command(insert_cmd)


	def get_table(self):
		return self.run_command(f"SELECT * FROM {self.table_name}")


	def get_columns(self):
		return self.run_command(f"SHOW COLUMNS FROM {self.table_name}")


	def run_command(self, cmd):
		try:
			self.cursor.execute(cmd)
		except connector.Error as err:
			print ('ERROR MESSAGE: ' + str(err.msg))
			print ('WITH ' + cmd)
		try:
			msg = self.cursor.fetchall()
		except:
			msg = self.cursor.fetchone()
		return msg


	def add_entry(self, name, price, description, link):
		cmd1 = f"INSERT INTO {self.table_name} (name, price, description, link)" + " "
		cmd2 = f"VALUES('{name}', '{price}', '{description}', '{link}');"
		self.run_command(cmd1 + cmd2)


	def delete_entry(self, row_id):
		cmd = f"DELETE FROM {self.table_name} WHERE id = {row_id};"
		self.run_command(cmd)


	def on_close(self):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()
