'''
dbname – the database name (database is a deprecated alias)
user – user name used to authenticate
password – password used to authenticate
host – database host address (defaults to UNIX socket if not provided)
port – connection port number (defaults to 5432 if not provided)

'''
import psycopg2

cursor=connection.cursor()
print(cursor)
