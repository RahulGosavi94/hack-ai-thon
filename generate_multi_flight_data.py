"""
Generate realistic passenger data for multiple disrupted flights with connecting passengers
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# Configuration - Multiple disrupted flights
DISRUPTED_FLIGHTS = [
    {
        "flight_number": "EY129",
        "origin": "DEL",
        "destination": "AUH",
        "passengers_total": 300,
        "passengers_with_connections": 250,
        "next_destinations": ["YYZ", "LHR", "SVO", "JFK", "ICN", "CDG", "BAH", "BEL"]
    },
    {
        "flight_number": "EY245",
        "origin": "BOM",
        "destination": "AUH",
        "passengers_total": 280,
        "passengers_with_connections": 230,
        "next_destinations": ["LHR", "JFK", "CDG", "FRA", "MUC", "ZRH", "LIS", "MAD"]
    },
    {
        "flight_number": "EY567",
        "origin": "KOL",
        "destination": "DXB",
        "passengers_total": 320,
        "passengers_with_connections": 260,
        "next_destinations": ["JFK", "LAX", "SFO", "YVR", "MEX", "MIA", "ORD", "DEN"]
    }
]

# Airline names
AIRLINES = ['Etihad Airways', 'Emirates', 'Qatar Airways', 'Air France', 'British Airways', 'Lufthansa']

# Generate passenger names
FIRST_NAMES = ['Rajesh', 'Priya', 'Ahmed', 'Sofia', 'John', 'Maria', 'James', 'Sarah', 'Michael', 'Emma', 
               'David', 'Anna', 'Robert', 'Lisa', 'William', 'Jennifer', 'Richard', 'Mary', 'Joseph', 'Patricia']
LAST_NAMES = ['Kumar', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
              'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson']

LOYALTY_TIERS = ['Guest', 'Silver', 'Gold', 'Platinum']
CABIN_CLASSES = ['Economy', 'Premium Economy', 'Business', 'First']

def generate_passengers_for_flights():
    all_passengers = []
    
    for flight_config in DISRUPTED_FLIGHTS:
        flight_number = flight_config["flight_number"]
        origin = flight_config["origin"]
        destination = flight_config["destination"]
        total_pax = flight_config["passengers_total"]
        pax_with_connections = flight_config["passengers_with_connections"]
        next_destinations = flight_config["next_destinations"]
        
        # Generate passengers with connecting flights
        for i in range(pax_with_connections):
            next_destination = random.choice(next_destinations)
            passenger = {
                "id": str(uuid.uuid4()),
                "dcsid": f"{uuid.uuid4().hex[:16].upper()}",
                "paxkey": f"{uuid.uuid4().hex}_{uuid.uuid4().hex}",
                "passenger_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "pnr": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}",
                "flight_number": flight_number,
                "flight_id": str(uuid.uuid4()),
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
                "segment_departure_iataCode": origin,
                "segment_arrival_iataCode": destination,
                "segment_departure_time": (datetime.now() + timedelta(hours=2)).isoformat() + "Z",
                "segment_arrival_time": (datetime.now() + timedelta(hours=11)).isoformat() + "Z",
                "segment_marketingFlightNumber": flight_number,
                # Next flight information
                "next_segment_departure_iataCode": destination,
                "next_segment_arrival_iataCode": next_destination,
                "next_segment_marketingFlightNumber": f"EY{random.randint(100, 999)}",
                "next_segment_departure_time": (datetime.now() + timedelta(hours=14)).isoformat() + "Z",
                "next_segment_arrival_time": (datetime.now() + timedelta(hours=22)).isoformat() + "Z",
                "passengerDisruptionStatus": "DISRUPTED",
                "Nationality": random.choice(["IND", "PAK", "AFG", "USA", "GBR", "FRA", "DEU", "RUS", "CHN", "JPN"]),
            }
            all_passengers.append(passenger)
        
        # Generate passengers ending at destination (no connections)
        for i in range(total_pax - pax_with_connections):
            passenger = {
                "id": str(uuid.uuid4()),
                "dcsid": f"{uuid.uuid4().hex[:16].upper()}",
                "paxkey": f"{uuid.uuid4().hex}_{uuid.uuid4().hex}",
                "passenger_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "pnr": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}",
                "flight_number": flight_number,
                "flight_id": str(uuid.uuid4()),
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
                "segment_departure_iataCode": origin,
                "segment_arrival_iataCode": destination,
                "segment_departure_time": (datetime.now() + timedelta(hours=2)).isoformat() + "Z",
                "segment_arrival_time": (datetime.now() + timedelta(hours=11)).isoformat() + "Z",
                "segment_marketingFlightNumber": flight_number,
                # No next flight - ending at destination
                "next_segment_departure_iataCode": None,
                "next_segment_arrival_iataCode": None,
                "next_segment_marketingFlightNumber": None,
                "passengerDisruptionStatus": "DISRUPTED",
                "Nationality": random.choice(["IND", "PAK", "AFG", "USA", "GBR", "FRA", "DEU", "RUS", "CHN", "JPN"]),
            }
            all_passengers.append(passenger)
    
    return all_passengers

def generate_flights_with_connections(passengers_by_destination):
    """Generate available flights for each destination"""
    flights_by_destination = {}
    
    for destination, count in passengers_by_destination.items():
        flights_by_destination[destination] = []
        
        for i in range(random.randint(4, 8)):
            flight = {
                "flight_number": f"EY{random.randint(100, 999)}",
                "airline_name": random.choice(AIRLINES),
                "origin": "HUB",  # Generic hub (AUH, DXB, etc)
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
    # Generate passengers for all flights
    all_passengers = generate_passengers_for_flights()
    
    # Group by next destination
    passengers_by_destination = {}
    for p in all_passengers:
        if p.get('next_segment_arrival_iataCode'):
            dest = p['next_segment_arrival_iataCode']
            if dest not in passengers_by_destination:
                passengers_by_destination[dest] = []
            passengers_by_destination[dest].append(p)
    
    print("=" * 80)
    print("MULTI-FLIGHT PASSENGER DATA GENERATED")
    print("=" * 80)
    print(f"\nTotal Passengers: {len(all_passengers)}")
    
    print("\n✅ Passengers by Flight:")
    for flight_config in DISRUPTED_FLIGHTS:
        flight_pax = [p for p in all_passengers if p['flight_number'] == flight_config['flight_number']]
        pax_with_conn = len([p for p in flight_pax if p.get('next_segment_arrival_iataCode')])
        pax_no_conn = len(flight_pax) - pax_with_conn
        print(f"  {flight_config['flight_number']}: {len(flight_pax)} passengers ({pax_with_conn} with connections, {pax_no_conn} ending at destination)")
    
    print("\nPassengers by next destination:")
    for dest, pax in sorted(passengers_by_destination.items()):
        print(f"  {dest}: {len(pax)} passengers")
    
    # Save passengers
    with open("test_data/passengers_data.json", "w") as f:
        json.dump(all_passengers, f, indent=2)
    
    print(f"\n✅ Saved {len(all_passengers)} passengers to test_data/passengers_data.json")
    
    # Generate and save available flights for each destination
    flights_by_dest = generate_flights_with_connections(passengers_by_destination)
    with open("test_data/available_flights.json", "w") as f:
        json.dump(flights_by_dest, f, indent=2)
    
    print(f"✅ Saved available flights to test_data/available_flights.json")
    
    # Create passenger messages tracking file
    passenger_messages = {}
    for p in all_passengers:
        passenger_messages[p['id']] = {
            "passenger_name": p['full_name'],
            "pnr": p['pnr'],
            "flight_number": p['flight_number'],
            "messages_sent": [],
            "actions_applied": []
        }
    
    with open("test_data/passenger_messages.json", "w") as f:
        json.dump(passenger_messages, f, indent=2)
    
    print(f"✅ Saved passenger messages tracking to test_data/passenger_messages.json")
    
    print("\n" + "=" * 80)
    print("DATA GENERATION COMPLETE")
    print("=" * 80)
