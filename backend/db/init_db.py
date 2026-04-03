import sqlite3

conn=sqlite3.connect("backend/db/policy.db")
cursor=conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS policies(id integer PRIMARY KEY autoincrement,category text UNIQUE,rule text)""")
cursor.execute("DELETE FROM policies")

cursor.execute("INSERT INTO policies (category,rule) values (?,?)",("food","Meals upto ₹1000 allowed. Alcohol is not reimbursable"))