
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from data.VehiculoPlusLocation import VehiculoPlusLocation
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Access variables from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
encoded_password = quote_plus(db_password)

uri = f"mongodb+srv://{db_user}:{encoded_password}@{db_server}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"

def double_newline():
    print("\n\t********************************************************")
    print("\n")

def ping_database(client: MongoClient)-> bool:
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        double_newline()
        return True
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        print(e)
        return False

def create_date_range_query(start_date: datetime, end_date: datetime)-> dict:
    # Create a query to find documents between the start and end dates
    query = {"timeStamp": {"$gte": start_date, "$lte": end_date}}
    return query

def print_results(location_data_list: list[VehiculoPlusLocation]):
    # Print the results
    for location_data in location_data_list:
        print(location_data)

# Display available placas with an integer identifier
def display_placas(placas: list[str]):
    print("Choose a vehicle to analyze:")
    for index, placa in enumerate(placas, 1):
        print(f"{index}. {placa}")

# Safely get user input for vehicle selection
def get_user_selection(placas: list[str]) -> str:
    print("")
    while True:
        try:
            choice = int(input("Enter the number corresponding to the vehicle: "))
            if 1 <= choice <= len(placas):
                return placas[choice - 1]
            else:
                print("Invalid number. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Show the menu with analysis options
def show_menu():
    print("\nSelect an option:")
    print("1. Graph time vs batteryPercentage")
    print("2. Graph time vs speed")
    print("3. Graph time vs locationAccuracy")
    print("4. Graph time vs speed and batteryPercentage")
    print("5. Graph time vs speed and locationAccuracy")
    print("6. Graph time vs batteryPercentage and locationAccuracy")
    print("7. Graph time vs speed, batteryPercentage, and locationAccuracy")
    print("9. Find the oldest and newest location reports")
    print("99. EXIT. Exit the program")

    double_newline()
    # Add more options as needed

    # Graph time vs batteryPercentage for a selected vehicle
def graph_time_vs_battery(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    times = [entry.timeStamp for entry in filtered_data]
    battery_percentages = [entry.batteryPercentage for entry in filtered_data]

    # Convert timeStamp to datetime for plotting if needed
    # (You can use datetime parsing if your time format is a string)

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%b %d, %Y, %I:%M %p")

    plt.figure(figsize=(10, 6))
    plt.plot(times, battery_percentages, marker='o', color='b', label='Battery %')
    plt.title(f'Time vs Battery Percentage for {placa} from {formatted_start} to {formatted_end}' )
    plt.xlabel('Time')
    plt.ylabel('Battery Percentage')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    double_newline()
    print("\t\t WELCOME, connecting to the database, please wait ... \n")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Ping the database
    if not ping_database(client):
        return  # Exit if the database cannot be reached

    # Access the database (already specified in the connection URI)
    db = client[db_name]

    # Access the collection
    collection = db['locations']

    start_date = datetime(2024, 11, 22, 17, 30, 0) # 2024-11-22 5:0:0 pm
    end_date = datetime(2024, 11, 25, 8, 30, 0)
    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%b %d, %Y, %I:%M %p")

    print("The selected date range is: \n")

    # Print the formatted dates
    print(f"Start Date: {formatted_start}")
    print(f"End Date: {formatted_end}")
    print("\nThe system will find all the vehicles that were active during this time period.")
    double_newline()

    print("\t\t Computing results, please wait ... \n\n")


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
    #print_results(location_data_list)

    print("The size of the list is: ", len(location_data_list))

    double_newline()
    print("Counting the number of times each vehicle appears in the data ... \n")

    # Sort location data by vehiculo.placa
    placa_counts  = Counter([location_data.vehiculo.placa for location_data in location_data_list])

    # Display results
    for placa, count in placa_counts.most_common():
        print(f"Placa: {placa}, Count: {count}")

    double_newline()
    placa_list = list(placa_counts.keys())

    display_placas(placa_list)

    double_newline()

    # Get the user's selection
    selected_placa = get_user_selection(placa_list)

    show_menu()

    try:
        option = int(input("Enter option number: "))
        if option == 1:
            graph_time_vs_battery(selected_placa, location_data_list, start_date, end_date)
        elif option == 99:
            print("Exiting the program ...")
        else:
            print("Option not implemented yet.")
    except ValueError:
        print("Invalid input. Please enter a valid option number.")


    #######################################################################################
    double_newline()
    # Close the connection
    print("Closing the connection to the database ...")
    client.close()
    print("END OF LINE")


if __name__ == "__main__":
    main()