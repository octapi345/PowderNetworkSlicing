from pymongo import MongoClient
import csv
import sys
import time

for i in range(100000):
    start=time.time()
    mongo_host = sys.argv[1]
    client = MongoClient(f"mongodb://{mongo_host}:27017")
    db = client['testdb']
    collection = db['testcollec']

    with open("/local/repository/testingdata.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        sum=0
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
        end = time.time()
        sum=1000*(end-start)
        print(f"{sum}ms")
        time.sleep(0.5)
