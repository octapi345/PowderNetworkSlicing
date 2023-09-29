from pymongo import MongoClient
import csv
client = MongoCient("mongodb://pc731.emulab.net:27017")

db = client['testdb']
collection = db['testcollec']

with open("data-j74tC1i3HTKxse01_GQho.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Convert the CSV row to a dictionary
        data = {
            "name": row["name"],
            "phone": row['phone'],
            "email": row["email"],
            "address": row['address'],
            "postalZip": int(row['postalZip']),
            "list": int(row['list']),
            "country": row['country']
        }

        # Insert the document into the collection
        collection.insert_one(data)
