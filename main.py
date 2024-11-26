
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Access variables from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
encoded_password = quote_plus(db_password)


uri = f"mongodb+srv://{db_user}:{encoded_password}@{db_server}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Access the database (already specified in the connection URI)
db = client[db_name]

# Access the collection
collection = db['locations']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

start_date = datetime(2024, 11, 22, 17, 0, 0) # 2024-11-22 5:0:0 pm
end_date = datetime(2024, 11, 25, 8, 0, 0)

query = {"timeStamp": {"$gte": start_date, "$lte": end_date}}
results = collection.find(query)

print("END OF LINE")






