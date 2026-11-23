
import json
import os

FILE_NAME = "trips.json"


# Load saved trips
def load_trips():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            print("Invalid data found. Starting with an empty list.")
            return []

    except (json.JSONDecodeError, OSError):
        print("Unable to read saved trips. Starting fresh.")
        return []


# Save trips to file
def save_trips(trips):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(trips, file, indent=4)
        return True
    except OSError:
        print("Error while saving the trip.")
        return False


# Get a non-empty text input
def get_text(message):
    while True:
        value = input(message).strip()

        if value:
            return value
        else:
            print("Input cannot be empty. Try again.")


# Get a valid positive number
def get_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount >= 0:
                return amount
            else:
                print("Amount cannot be negative.")

        except ValueError:
            print("Please enter a valid number.")


# Add a new trip
def add_trip(trips):
    print("\n--- Add New Trip ---")

    destination = get_text("Enter destination: ")
    transport = get_amount("Transport cost: ₹")
    stay = get_amount("Stay cost: ₹")
    food = get_amount("Food cost: ₹")
    activities = get_amount("Activity cost: ₹")

    total = transport + stay + food + activities

    trip = {
        "destination": destination,
        "transport": transport,
        "stay": stay,
        "food": food,
        "activities": activities,
        "total": total
    }

    trips.append(trip)

    if save_trips(trips):
        print("\nTrip saved successfully!")
        print("Destination:", destination)
        print(f"Total estimated budget: ₹{total:.2f}")


# Display all trips
def view_trips(trips):
    print("\n--- Saved Trips ---")

    if not trips:
        print("No trips available.")
        return

    for i, trip in enumerate(trips, start=1):
        print(f"\nTrip {i}")
        print("Destination:", trip["destination"])
        print(f"Transport: ₹{trip['transport']:.2f}")
        print(f"Stay: ₹{trip['stay']:.2f}")
        print(f"Food: ₹{trip['food']:.2f}")
        print(f"Activities: ₹{trip['activities']:.2f}")
        print(f"Total: ₹{trip['total']:.2f}")


# Search trips by destination
def search_trip(trips):
    print("\n--- Search Trip ---")

    keyword = get_text("Enter destination to search: ").lower()
    found = False

    for trip in trips:
        if keyword in trip["destination"].lower():
            print("\nDestination:", trip["destination"])
            print(f"Total budget: ₹{trip['total']:.2f}")
            found = True

    if not found:
        print("No matching trip found.")


# Delete a trip
def delete_trip(trips):
    print("\n--- Delete Trip ---")

    if not trips:
        print("No trips to delete.")
        return

    view_trips(trips)

    try:
        number = int(input("\nEnter trip number to delete: "))

        if 1 <= number <= len(trips):
            removed_trip = trips.pop(number - 1)

            if save_trips(trips):
                print(removed_trip["destination"], "trip deleted successfully.")
        else:
            print("Invalid trip number.")

    except ValueError:
        print("Please enter a valid number.")


# Display budget summary
def budget_summary(trips):
    print("\n--- Budget Summary ---")

    if not trips:
        print("No trip data available.")
        return

    total_budget = sum(trip["total"] for trip in trips)
    average_budget = total_budget / len(trips)

    highest_trip = max(trips, key=lambda trip: trip["total"])
    lowest_trip = min(trips, key=lambda trip: trip["total"])

    print("Number of trips:", len(trips))
    print(f"Total budget of all trips: ₹{total_budget:.2f}")
    print(f"Average trip budget: ₹{average_budget:.2f}")
    print("Highest budget trip:", highest_trip["destination"])
    print(f"Highest amount: ₹{highest_trip['total']:.2f}")
    print("Lowest budget trip:", lowest_trip["destination"])
    print(f"Lowest amount: ₹{lowest_trip['total']:.2f}")


# Export a simple text report
def export_report(trips):
    print("\n--- Export Report ---")

    if not trips:
        print("No trip data available to export.")
        return

    try:
        with open("trip_report.txt", "w") as file:
            file.write("CAMPUSSOLVE - TRIP BUDGET REPORT\n")
            file.write("=" * 35 + "\n\n")

            for i, trip in enumerate(trips, start=1):
                file.write(f"Trip {i}: {trip['destination']}\n")
                file.write(f"Transport: ₹{trip['transport']:.2f}\n")
                file.write(f"Stay: ₹{trip['stay']:.2f}\n")
                file.write(f"Food: ₹{trip['food']:.2f}\n")
                file.write(f"Activities: ₹{trip['activities']:.2f}\n")
                file.write(f"Total: ₹{trip['total']:.2f}\n")
                file.write("-" * 35 + "\n")

            overall_total = sum(trip["total"] for trip in trips)
            file.write(f"\nOverall Budget: ₹{overall_total:.2f}\n")

        print("Report exported as trip_report.txt")

    except OSError:
        print("Unable to export report.")


# Main menu
def main():
    trips = load_trips()

    while True:
        print("\n================================")
        print("   CAMPUSSOLVE - TRIP BUDGET")
        print("================================")
        print("1. Add New Trip")
        print("2. View All Trips")
        print("3. Search Trip")
        print("4. Delete Trip")
        print("5. Budget Summary")
        print("6. Export Report")
        print("7. Exit")
        print("================================")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_trip(trips)

        elif choice == "2":
            view_trips(trips)

        elif choice == "3":
            search_trip(trips)

        elif choice == "4":
            delete_trip(trips)

        elif choice == "5":
            budget_summary(trips)

        elif choice == "6":
            export_report(trips)

        elif choice == "7":
            print("Thank you for using CampusSolve calculator!")
            break

        else:
            print("Invalid choice. Please select from 1 to 7.")


# Start the program
if __name__ == "__main__":
    main()
