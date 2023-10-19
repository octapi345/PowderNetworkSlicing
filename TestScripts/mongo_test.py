from pymongo import MongoClient
import csv
client = MongoClient("mongodb://nfs.octapi-169709.networkslicing.emulab.net:27017")

db = client['testdb']
collection = db['testcollec']

with open("../testdata.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Convert the CSV row to a dictionary
        data = {
            "name": row["name"],
            "phone": row['phone'],
            "email": row["email"],
            "address": row['address'],
            "postalZip": row['postalZip'],
            "list": int(row['list']),
            "country": row['country']
        }

        # Insert the document into the collection
        collection.insert_one(data)
