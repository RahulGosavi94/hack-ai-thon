"""
Generate realistic passenger data with connecting flights
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# Configuration
DISRUPTED_FLIGHT = "EY129"  # DEL -> AUH
DISRUPTION_ORIGIN = "DEL"
DISRUPTION_DESTINATION = "AUH"
TOTAL_PASSENGERS = 300
PASSENGERS_WITH_CONNECTIONS = 250
PASSENGERS_ENDING_AT_AUH = 50

# Next destinations for connecting passengers
NEXT_DESTINATIONS = ['YYZ', 'LHR', 'SVO', 'JFK', 'ICN', 'CDG', 'BAH', 'BEL']

# Airline names
AIRLINES = ['Etihad Airways', 'Emirates', 'Qatar Airways', 'Air France', 'British Airways', 'Lufthansa']

# Generate passenger names
FIRST_NAMES = ['Rajesh', 'Priya', 'Ahmed', 'Sofia', 'John', 'Maria', 'James', 'Sarah', 'Michael', 'Emma', 
               'David', 'Anna', 'Robert', 'Lisa', 'William', 'Jennifer', 'Richard', 'Mary', 'Joseph', 'Patricia']
LAST_NAMES = ['Kumar', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
              'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson']

LOYALTY_TIERS = ['Guest', 'Silver', 'Gold', 'Platinum']
CABIN_CLASSES = ['Economy', 'Premium Economy', 'Business', 'First']

def generate_passengers():
    passengers = []
    
    # Generate passengers with connecting flights
    for i in range(PASSENGERS_WITH_CONNECTIONS):
        next_destination = random.choice(NEXT_DESTINATIONS)
        passenger = {
            "id": str(uuid.uuid4()),
            "dcsid": f"{uuid.uuid4().hex[:16].upper()}",
            "paxkey": f"{uuid.uuid4().hex}_{uuid.uuid4().hex}",
            "passenger_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "pnr": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}",
            "flight_number": DISRUPTED_FLIGHT,
            "flight_id": "cb5cd224-b4e9-412a-838d-b56184607281",  # EY129
            "email": f"passenger{i}@example.com",
            "passenger_title": random.choice(['Mr.', 'Ms.', 'Mrs.', 'Dr.']),
            "passenger_gender": random.choice(['MALE', 'FEMALE']),
            "passenger_flightPassengerType": random.choice(['ADULT', 'CHILD']),
            "loyalty_tier": random.choice(LOYALTY_TIERS),
            "fare_class": random.choice(['E', 'Y', 'J', 'F']),
            "fare_class_name": random.choice(CABIN_CLASSES),
            "seat_number": f"{random.randint(1, 50):02d}{random.choice('ABCDEF')}",
            "special_service_request": random.choice([None, "WHEELCHAIR", "VEGETARIAN", "UNACCOMPANIED_MINOR", None, None]),
            "contactsEmail": f"passenger{i}@example.com",
            "processed_date": datetime.now().strftime("%Y-%m-%d"),
            "processed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "segment_departure_iataCode": DISRUPTION_ORIGIN,
            "segment_arrival_iataCode": DISRUPTION_DESTINATION,
            "segment_departure_time": (datetime.now() + timedelta(hours=2)).isoformat() + "Z",
            "segment_arrival_time": (datetime.now() + timedelta(hours=11)).isoformat() + "Z",
            "segment_marketingFlightNumber": DISRUPTED_FLIGHT,
            # Next flight information
            "next_segment_departure_iataCode": DISRUPTION_DESTINATION,
            "next_segment_arrival_iataCode": next_destination,
            "next_segment_marketingFlightNumber": f"EY{random.randint(100, 999)}",
            "next_segment_departure_time": (datetime.now() + timedelta(hours=14)).isoformat() + "Z",
            "next_segment_arrival_time": (datetime.now() + timedelta(hours=22)).isoformat() + "Z",
            "next_legDeliveries_operatingFlight_number": f"{random.randint(100, 999)}",
            "passengerDisruptionStatus": "DISRUPTED",
            "Nationality": random.choice(["IND", "PAK", "AFG", "USA", "GBR", "FRA", "DEU", "RUS", "CHN", "JPN"]),
        }
        passengers.append(passenger)
    
    # Generate passengers ending at AUH
    for i in range(PASSENGERS_WITH_CONNECTIONS, TOTAL_PASSENGERS):
        passenger = {
            "id": str(uuid.uuid4()),
            "dcsid": f"{uuid.uuid4().hex[:16].upper()}",
            "paxkey": f"{uuid.uuid4().hex}_{uuid.uuid4().hex}",
            "passenger_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "pnr": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}",
            "flight_number": DISRUPTED_FLIGHT,
            "flight_id": "cb5cd224-b4e9-412a-838d-b56184607281",
            "email": f"passenger{i}@example.com",
            "passenger_title": random.choice(['Mr.', 'Ms.', 'Mrs.', 'Dr.']),
            "passenger_gender": random.choice(['MALE', 'FEMALE']),
            "passenger_flightPassengerType": random.choice(['ADULT', 'CHILD']),
            "loyalty_tier": random.choice(LOYALTY_TIERS),
            "fare_class": random.choice(['E', 'Y', 'J', 'F']),
            "fare_class_name": random.choice(CABIN_CLASSES),
            "seat_number": f"{random.randint(1, 50):02d}{random.choice('ABCDEF')}",
            "special_service_request": None,
            "contactsEmail": f"passenger{i}@example.com",
            "processed_date": datetime.now().strftime("%Y-%m-%d"),
            "processed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "segment_departure_iataCode": DISRUPTION_ORIGIN,
            "segment_arrival_iataCode": DISRUPTION_DESTINATION,
            "segment_departure_time": (datetime.now() + timedelta(hours=2)).isoformat() + "Z",
            "segment_arrival_time": (datetime.now() + timedelta(hours=11)).isoformat() + "Z",
            "segment_marketingFlightNumber": DISRUPTED_FLIGHT,
            # No next flight - ending in AUH
            "next_segment_departure_iataCode": None,
            "next_segment_arrival_iataCode": None,
            "next_segment_marketingFlightNumber": None,
            "passengerDisruptionStatus": "DISRUPTED",
            "Nationality": random.choice(["IND", "PAK", "AFG", "USA", "GBR", "FRA", "DEU", "RUS", "CHN", "JPN"]),
        }
        passengers.append(passenger)
    
    return passengers

def generate_flights_with_connections(passengers_by_destination):
    """Generate available flights for each destination"""
    flights_by_destination = {}
    
    for destination, count in passengers_by_destination.items():
        flights_by_destination[destination] = []
        
        for i in range(random.randint(4, 8)):
            flight = {
                "flight_number": f"EY{random.randint(100, 999)}",
                "airline_name": random.choice(AIRLINES),
                "origin": DISRUPTION_DESTINATION,
                "destination": destination,
                "departure_time": f"{random.randint(8, 22):02d}:{random.randint(0, 59):02d}",
                "duration": f"{random.randint(8, 16)}h {random.randint(0, 59):02d}m",
                "cabin": random.choice(CABIN_CLASSES),
                "available_seats": random.randint(5, 150),
                "price": random.randint(150, 1200),
                "codeshare": random.choice([True, False, False]),
                "partner": random.choice(["BA", "LH", "AF", "QR", "EK", None]) if random.random() > 0.6 else None
            }
            flights_by_destination[destination].append(flight)
    
    return flights_by_destination

if __name__ == "__main__":
    # Generate passengers
    passengers = generate_passengers()
    
    # Group by next destination
    passengers_by_destination = {}
    for p in passengers:
        if p.get('next_segment_arrival_iataCode'):
            dest = p['next_segment_arrival_iataCode']
            if dest not in passengers_by_destination:
                passengers_by_destination[dest] = []
            passengers_by_destination[dest].append(p)
    
    print("=" * 80)
    print("PASSENGER DATA GENERATED")
    print("=" * 80)
    print(f"\nTotal Passengers: {len(passengers)}")
    print(f"Passengers with connections: {PASSENGERS_WITH_CONNECTIONS}")
    print(f"Passengers ending at AUH: {PASSENGERS_ENDING_AT_AUH}")
    
    print("\nPassengers by next destination:")
    for dest, pax in sorted(passengers_by_destination.items()):
        print(f"  {dest}: {len(pax)} passengers")
    
    # Save passengers
    with open("test_data/passengers_data.json", "w") as f:
        json.dump(passengers, f, indent=2)
    
    print(f"\n✅ Saved {len(passengers)} passengers to test_data/passengers_data.json")
    
    # Generate and save available flights for each destination
    flights_by_dest = generate_flights_with_connections(passengers_by_destination)
    with open("test_data/available_flights.json", "w") as f:
        json.dump(flights_by_dest, f, indent=2)
    
    print(f"✅ Saved available flights to test_data/available_flights.json")
    
    # Create passenger messages tracking file
    passenger_messages = {}
    for p in passengers:
        passenger_messages[p['id']] = {
            "passenger_name": p['full_name'],
            "pnr": p['pnr'],
            "messages_sent": [],
            "actions_applied": []
        }
    
    with open("test_data/passenger_messages.json", "w") as f:
        json.dump(passenger_messages, f, indent=2)
    
    print(f"✅ Saved passenger messages tracking to test_data/passenger_messages.json")
    
    print("\n" + "=" * 80)
    print("DATA GENERATION COMPLETE")
    print("=" * 80)
