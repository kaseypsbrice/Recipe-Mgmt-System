import psycopg2

conn = psycopg2.connect(database="irms", 
                        host="localhost", 
                        user="irms_admin", 
                        password="admin", 
                        port="5432")
# Initialises a database session

cursor = conn.cursor()

cursor.execute("SELECT * FROM users")

print(cursor.fetchall())
# Will fetch all rows that the query returns
# fetchone() can be used to just fetch one row