import csv 
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "book"
)

query = "INSERT INTO book_list(isbn , title , author , year ) VALUES(%s,%s,%s,%s)"
mycur = mydb.cursor()

with open("books.csv" , 'r') as csv_file : 
    reader = csv.reader(csv_file , delimiter = ',' )
    for row in reader :
        val = (row[0] , row[1] , row[2] , row[3] )
        mycur.execute(query , val)
        mydb.commit()

        
    

