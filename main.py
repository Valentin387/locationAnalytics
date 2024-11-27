
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from data.VehiculoPlusLocation import VehiculoPlusLocation

# Load environment variables
load_dotenv()

# Access variables from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
encoded_password = quote_plus(db_password)

uri = f"mongodb+srv://{db_user}:{encoded_password}@{db_server}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"

def ping_database(client: MongoClient)-> bool:
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        print("\n ************************************************** \n\n")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        print(e)

def create_date_range_query(start_date: datetime, end_date: datetime)-> dict:
    # Create a query to find documents between the start and end dates
    query = {"timeStamp": {"$gte": start_date, "$lte": end_date}}
    return query


if __name__ == "__main__":
    print("\n ************************************************** \n\n")
    print("WELCOME, computing results, please wait ... \n\n")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Ping the database
    ping_database(client)

    # Access the database (already specified in the connection URI)
    db = client[db_name]

    # Access the collection
    collection = db['locations']

    start_date = datetime(2024, 11, 26, 21, 0, 0) # 2024-11-22 5:0:0 pm
    end_date = datetime(2024, 11, 26, 21, 30, 0)

        # Create the query
    query = create_date_range_query(start_date, end_date)

    results = collection.find(query)

    # List to hold the LocationData objects
    location_data_list : list[VehiculoPlusLocation] = []

    # Convert each MongoDB document into a VehiculoPlusLocation object and append to the list
    for document in results:
        # Convert MongoDB document to VehiculoPlusLocation object
        location_data = VehiculoPlusLocation(**document)
        location_data_list.append(location_data)

    # Print the results
    for location_data in location_data_list:
        print(location_data)

    print("The size of the list is: ", len(location_data_list))

    print("\n ************************************************** \n\n")
    print("END OF LINE")


