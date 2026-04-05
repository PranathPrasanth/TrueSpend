import sqlite3

conn=sqlite3.connect("policy.db")
cursor=conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS policies(id integer PRIMARY KEY autoincrement,category text UNIQUE,rule text)""")
cursor.execute("DELETE FROM policies")

cursor.execute("INSERT INTO policies (category,rule) values (?,?)",("food","Meals upto ₹1000 allowed. Alcohol is not reimbursable."))

cursor.execute("INSERT into policies (category,rule) VALUES (?,?)",("travel","Taxi expenses allowed upto ₹2000."))

cursor.execute("INSERT INTO policies (category,rule) VALUES (?,?)",("accommodation","Hotel stay allowed up to ₹5000 per night."))

conn.commit()
conn.close()

print("Database initialized!")