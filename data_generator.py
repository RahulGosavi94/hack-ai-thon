"""
Data Generator for Airline Disruption Management System
Generates realistic flight and passenger data for 15 flights over 2 days
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

# Constants
AIRLINES = ["EY"]  # Etihad Airways
AIRCRAFT_TYPES = ["A380", "B787-9", "B787-10", "A350-900", "B777-300ER", "A321neo"]
FARE_CLASSES = ["J", "C", "W", "Y", "B", "H", "K", "M", "L", "V", "T", "Q"]

# Disruption statuses and reasons
DISRUPTION_STATUSES = ["On Time", "Delayed", "Cancelled", "Diverted", "Aircraft Swap"]
DISRUPTION_REASONS = {
    "Delayed": [
        "Weather Conditions",
        "Technical Issue",
        "Crew Availability",
        "Air Traffic Control Delay",
        "Late Incoming Aircraft",
        "Operational Reasons",
        "Airport Congestion",
        "Bird Strike",
        "Refueling Delay",
        "Catering Delay"
    ],
    "Cancelled": [
        "Severe Weather",
        "Aircraft Technical Fault",
        "Crew Shortage",
        "Airport Closure",
        "Security Threat",
        "Operational Decision",
        "Aircraft Maintenance"
    ],
    "Diverted": [
        "Weather at Destination",
        "Medical Emergency",
        "Airport Closure at Destination",
        "Technical Issue",
        "Security Incident"
    ],
    "Aircraft Swap": [
        "Technical Issue with Original Aircraft",
        "Maintenance Requirements",
        "Operational Optimization",
        "Aircraft Availability"
    ]
}
FARE_CLASS_NAMES = {
    "J": "Business First",
    "C": "Business",
    "W": "Premium Economy",
    "Y": "Economy Flex",
    "B": "Economy Standard",
    "H": "Economy Saver",
    "K": "Economy Super Saver",
    "M": "Economy Promo",
    "L": "Economy Light",
    "V": "Economy Value",
    "T": "Economy Basic",
    "Q": "Economy Restricted"
}

# Etihad major routes
ROUTES = [
    {"origin": "AUH", "destination": "LHR", "duration": 420},  # Abu Dhabi to London
    {"origin": "AUH", "destination": "JFK", "duration": 840},  # Abu Dhabi to New York
    {"origin": "AUH", "destination": "SYD", "duration": 820},  # Abu Dhabi to Sydney
    {"origin": "AUH", "destination": "BOM", "duration": 180},  # Abu Dhabi to Mumbai
    {"origin": "AUH", "destination": "DXB", "duration": 60},   # Abu Dhabi to Dubai
    {"origin": "AUH", "destination": "DOH", "duration": 60},   # Abu Dhabi to Doha
    {"origin": "AUH", "destination": "CDG", "duration": 400},  # Abu Dhabi to Paris
    {"origin": "AUH", "destination": "FRA", "duration": 380},  # Abu Dhabi to Frankfurt
    {"origin": "AUH", "destination": "SIN", "duration": 450},  # Abu Dhabi to Singapore
    {"origin": "AUH", "destination": "BKK", "duration": 360},  # Abu Dhabi to Bangkok
    {"origin": "AUH", "destination": "MEL", "duration": 780},  # Abu Dhabi to Melbourne
    {"origin": "AUH", "destination": "MAD", "duration": 420},  # Abu Dhabi to Madrid
    {"origin": "AUH", "destination": "MAN", "duration": 410},  # Abu Dhabi to Manchester
    {"origin": "AUH", "destination": "LAX", "duration": 900},  # Abu Dhabi to Los Angeles
    {"origin": "AUH", "destination": "ICN", "duration": 480},  # Abu Dhabi to Seoul
]

FIRST_NAMES = [
    "Mohammed", "Ahmed", "Fatima", "Sarah", "John", "Michael", "David", "James", "Robert",
    "William", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra", "Ashley", "Kimberly",
    "Emily", "Donna", "Michelle", "Carol", "Amanda", "Dorothy", "Melissa", "Deborah", "Stephanie",
    "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna",
    "Brenda", "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra",
    "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather", "Diane", "Ruth", "Julie",
    "Olivia", "Joyce", "Virginia", "Victoria", "Kelly", "Lauren", "Christina", "Joan", "Evelyn",
    "Judith", "Megan", "Andrea", "Cheryl", "Hannah", "Jacqueline", "Martha", "Gloria", "Teresa"
]

LAST_NAMES = [
    "Al Maktoum", "Al Nahyan", "Khan", "Ahmed", "Ali", "Hassan", "Hussein", "Smith", "Johnson",
    "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez",
    "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis",
    "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
    "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker"
]

MEAL_PREFERENCES = ["VGML", "HNML", "MOML", "KSML", "AVML", "VLML", "BBML", "CHML", "DBML", "FPML", "GFML", "LCML", "LFML", "LPML", "LSML", "NLML", "ORML", "PRML", "SFML", "VJML", None]
SPECIAL_SERVICES = ["WCHR", "WCHC", "WCHS", "WCMP", "WCBD", "WCBW", "DEAF", "BLND", "DPNA", "UMNR", "PETC", "ESAN", "MAAS", None]

NATIONALITIES = ["AE", "US", "GB", "IN", "PK", "BD", "PH", "EG", "SA", "DE", "FR", "CN", "AU", "CA", "IT", "ES", "NL", "SE", "NO", "DK"]

def generate_pnr():
    """Generate a realistic 6-character PNR"""
    return ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=6))

def generate_ticket_number(airline="607"):
    """Generate a 13-digit ticket number"""
    return f"{airline}{random.randint(1000000000, 9999999999)}"

def generate_flight_number():
    """Generate Etihad flight number"""
    return f"EY{random.randint(1, 999):03d}"

def generate_flight_data(flight_index: int, flight_date: datetime) -> Dict:
    """Generate flight data"""
    route = ROUTES[flight_index % len(ROUTES)]
    flight_number = generate_flight_number()
    aircraft_type = random.choice(AIRCRAFT_TYPES)
    
    # Set departure time between 00:00 and 23:00
    departure_hour = random.randint(0, 23)
    departure_minute = random.choice([0, 15, 30, 45])
    
    std = flight_date.replace(hour=departure_hour, minute=departure_minute, second=0)
    sta = std + timedelta(minutes=route["duration"])
    
    # Determine disruption status (70% on time, 20% delayed, 5% cancelled, 3% aircraft swap, 2% diverted)
    disruption_weights = [70, 20, 5, 3, 2]
    disruption_status = random.choices(DISRUPTION_STATUSES, weights=disruption_weights)[0]
    
    # Set disruption reason based on status
    disruption_reason = None
    delay_minutes = 0
    
    if disruption_status in DISRUPTION_REASONS:
        disruption_reason = random.choice(DISRUPTION_REASONS[disruption_status])
        
        # Set delay for delayed flights
        if disruption_status == "Delayed":
            # Delays range from 15 minutes to 6 hours
            delay_minutes = random.choice([15, 30, 45, 60, 90, 120, 150, 180, 240, 300, 360])
    
    # Calculate estimated times based on disruption
    etd = std + timedelta(minutes=delay_minutes)
    eta = sta + timedelta(minutes=delay_minutes)
    
    # For cancelled flights, set status accordingly
    flight_status = "Cancelled" if disruption_status == "Cancelled" else "Scheduled" if disruption_status == "On Time" else "Delayed"
    
    # Gate assignment
    gate = f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 40)}"
    
    # Seat configuration based on aircraft
    seat_config = {
        "A380": {"J": 8, "C": 70, "W": 40, "Y": 330},
        "B787-9": {"J": 28, "C": 0, "W": 21, "Y": 200},
        "B787-10": {"J": 32, "C": 0, "W": 21, "Y": 240},
        "A350-900": {"J": 44, "C": 0, "W": 21, "Y": 210},
        "B777-300ER": {"J": 8, "C": 42, "W": 28, "Y": 240},
        "A321neo": {"J": 16, "C": 0, "W": 0, "Y": 144}
    }
    
    return {
        "flight_id": str(uuid.uuid4()),
        "flight_number": flight_number,
        "airline": "EY",
        "aircraft_type": aircraft_type,
        "aircraft_registration": f"A6-{random.choice(['ETH', 'EYB', 'EYC', 'EYD', 'EYE', 'EYF'])}{random.randint(1, 99):02d}",
        "origin": route["origin"],
        "destination": route["destination"],
        "scheduled_departure": std.isoformat(),
        "scheduled_arrival": sta.isoformat(),
        "estimated_departure": etd.isoformat(),
        "estimated_arrival": eta.isoformat(),
        "gate": gate,
        "terminal": "3",
        "status": flight_status,
        "disruption_status": disruption_status,
        "disruption_reason": disruption_reason,
        "delay_minutes": delay_minutes if disruption_status == "Delayed" else 0,
        "seat_configuration": seat_config[aircraft_type],
        "flight_date": flight_date.strftime("%Y-%m-%d")
    }

def generate_passenger(flight: Dict, passenger_index: int) -> Dict:
    """Generate realistic passenger data"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    # Determine fare class based on aircraft configuration
    seat_config = flight["seat_configuration"]
    fare_class_distribution = []
    for cabin, seats in seat_config.items():
        fare_class_distribution.extend([cabin] * seats)
    
    fare_class = random.choice(fare_class_distribution) if fare_class_distribution else "Y"
    
    # Assign seat
    if fare_class == "J":
        seat = f"{random.randint(1, 2)}{random.choice(['A', 'D', 'G', 'K'])}"
    elif fare_class == "C":
        seat = f"{random.randint(6, 15)}{random.choice(['A', 'D', 'G', 'K'])}"
    elif fare_class == "W":
        seat = f"{random.randint(16, 20)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'H', 'J', 'K'])}"
    else:
        seat = f"{random.randint(25, 60)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K'])}"
    
    # Loyalty tier
    loyalty_tiers = ["Guest", "Silver", "Gold", "Platinum", None]
    loyalty_weights = [50, 25, 15, 10, 0]
    loyalty_tier = random.choices(loyalty_tiers, weights=loyalty_weights)[0]
    
    # Frequent flyer number
    ff_number = f"EY{random.randint(100000000, 999999999)}" if loyalty_tier else None
    
    # Special services (10% chance)
    ssr = random.choice(SPECIAL_SERVICES) if random.random() < 0.1 else None
    
    # Meal preference (80% chance)
    meal = random.choice(MEAL_PREFERENCES) if random.random() < 0.8 else None
    
    # Baggage
    if fare_class in ["J", "C"]:
        checked_bags = random.randint(2, 3)
        baggage_weight = random.randint(40, 70)
    elif fare_class == "W":
        checked_bags = random.randint(1, 2)
        baggage_weight = random.randint(23, 46)
    else:
        checked_bags = random.randint(0, 2)
        baggage_weight = random.randint(0, 46)
    
    # Contact info
    country_code = random.choice(["+971", "+1", "+44", "+91", "+92", "+880", "+63", "+20", "+966"])
    phone = f"{country_code}{random.randint(100000000, 9999999999)}"
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com'])}"
    
    # Ticket price
    base_prices = {"J": 5000, "C": 3000, "W": 1500, "Y": 800, "B": 600, "H": 450, "K": 350, "M": 300, "L": 250, "V": 220, "T": 200, "Q": 180}
    base_price = base_prices.get(fare_class, 500)
    ticket_price = base_price + random.randint(-100, 200)
    
    return {
        "passenger_id": str(uuid.uuid4()),
        "pnr": generate_pnr(),
        "ticket_number": generate_ticket_number(),
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "email": email,
        "phone": phone,
        "nationality": random.choice(NATIONALITIES),
        "passport_number": f"{random.choice(NATIONALITIES)}{random.randint(100000, 9999999)}",
        "date_of_birth": (datetime.now() - timedelta(days=random.randint(6570, 25550))).strftime("%Y-%m-%d"),
        "fare_class": fare_class,
        "fare_class_name": FARE_CLASS_NAMES.get(fare_class, "Economy"),
        "seat_number": seat,
        "frequent_flyer_number": ff_number,
        "loyalty_tier": loyalty_tier,
        "special_service_request": ssr,
        "meal_preference": meal,
        "checked_bags": checked_bags,
        "baggage_weight_kg": baggage_weight,
        "ticket_price_usd": ticket_price,
        "booking_date": (datetime.fromisoformat(flight["scheduled_departure"]) - timedelta(days=random.randint(1, 120))).isoformat(),
        "check_in_status": random.choice(["Not Checked In", "Checked In", "Checked In"]) if random.random() < 0.7 else "Not Checked In",
        "boarding_pass_issued": random.choice([True, False]) if random.random() < 0.6 else False,
        "flight_id": flight["flight_id"],
        "flight_number": flight["flight_number"],
        "origin": flight["origin"],
        "destination": flight["destination"],
        "scheduled_departure": flight["scheduled_departure"]
    }

def generate_dataset():
    """Generate complete dataset"""
    # Get today and tomorrow
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    all_flights = []
    all_passengers = []
    all_bookings = []
    all_disruptions = []
    all_resources = []

    # Generate 15 flights (7-8 today, 7-8 tomorrow)
    for i in range(15):
        flight_date = today if i < 8 else tomorrow
        flight = generate_flight_data(i, flight_date)
        all_flights.append(flight)

        # Generate 300-350 passengers per flight
        num_passengers = random.randint(300, 350)
        for j in range(num_passengers):
            passenger = generate_passenger(flight, j)
            all_passengers.append(passenger)

            # Booking/Itinerary Entity
            booking = {
                "booking_id": str(uuid.uuid4()),
                "pnr": passenger["pnr"],
                "origin": passenger["origin"],
                "destination": passenger["destination"],
                "passenger_id": passenger["passenger_id"],
                "flight_segments": [
                    {
                        "flight_number": passenger["flight_number"],
                        "origin": passenger["origin"],
                        "destination": passenger["destination"],
                        "scheduled_departure": passenger["scheduled_departure"],
                        "scheduled_arrival": flight["scheduled_arrival"]
                    }
                ],
                "connection_times": [],
                "fare_rules": "Refundable, change fee applies",
                "penalties": "Change fee $100",
                "interline_agreements": ["EY", "QR", "EK"]
            }
            all_bookings.append(booking)

    # Disruption Event Entity (sample: 1 per flight with disruption)
    for flight in all_flights:
        if flight["disruption_status"] != "On Time":
            disruption = {
                "disruption_id": str(uuid.uuid4()),
                "event_type": flight["disruption_status"],
                "event_start_time": flight["scheduled_departure"],
                "reason_code": flight["disruption_reason"] or "Operational",
                "estimated_recovery_time": flight["estimated_departure"],
                "resources_needed": ["Hotel", "Meal", "Transport"] if flight["disruption_status"] in ["Delayed", "Cancelled"] else [],
                "flight_id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "affected_passenger_ids": [p["passenger_id"] for p in all_passengers if p["flight_id"] == flight["flight_id"]]
            }
            all_disruptions.append(disruption)

    # Resource Entity (sample hotel, meal, transport, compensation)
    for i in range(5):
        resource = {
            "resource_id": str(uuid.uuid4()),
            "resource_type": random.choice(["Hotel", "Meal", "Transport", "Compensation"]),
            "hotel": {
                "rooms_available": random.randint(10, 100),
                "location": random.choice(["Airport Hotel", "City Center", "Near Terminal"]),
                "cost_per_night": round(random.uniform(80, 250), 2)
            },
            "meal": {
                "voucher_amount": round(random.uniform(10, 50), 2),
                "availability": random.choice(["Breakfast", "Lunch", "Dinner", "24/7"]),
                "time_of_day_rules": "Valid for delays over 3 hours"
            },
            "transport": {
                "bus_available": random.choice([True, False]),
                "cost": round(random.uniform(5, 30), 2)
            },
            "compensation": {
                "rule": random.choice(["EC261", "UAE", "Local"]),
                "amount": round(random.uniform(200, 600), 2)
            }
        }
        all_resources.append(resource)

    return {
        "flights": all_flights,
        "passengers": all_passengers,
        "bookings": all_bookings,
        "disruptions": all_disruptions,
        "resources": all_resources,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_flights": len(all_flights),
            "total_passengers": len(all_passengers),
            "flights_today": sum(1 for f in all_flights if f["flight_date"] == today.strftime("%Y-%m-%d")),
            "flights_tomorrow": sum(1 for f in all_flights if f["flight_date"] == tomorrow.strftime("%Y-%m-%d")),
            "total_bookings": len(all_bookings),
            "total_disruptions": len(all_disruptions),
            "total_resources": len(all_resources)
        }
    }

def generate_summary(dataset: Dict) -> str:
    """Generate human-readable summary"""
    flights = dataset["flights"]
    passengers = dataset["passengers"]
    
    # Group passengers by flight
    flight_passenger_count = {}
    for passenger in passengers:
        flight_id = passenger["flight_id"]
        if flight_id not in flight_passenger_count:
            flight_passenger_count[flight_id] = 0
        flight_passenger_count[flight_id] += 1
    
    summary_lines = []
    # Calculate disruption statistics
    disruption_counts = {}
    for flight in flights:
        status = flight["disruption_status"]
        if status not in disruption_counts:
            disruption_counts[status] = 0
        disruption_counts[status] += 1
    
    summary_lines.append("=" * 100)
    summary_lines.append("AIRLINE DISRUPTION MANAGEMENT SYSTEM - FLIGHT & PASSENGER DATA SUMMARY")
    summary_lines.append("=" * 100)
    summary_lines.append(f"\nGenerated at: {dataset['generated_at']}")
    summary_lines.append(f"Total Flights: {dataset['summary']['total_flights']}")
    summary_lines.append(f"Total Passengers: {dataset['summary']['total_passengers']}")
    summary_lines.append(f"Average Passengers per Flight: {dataset['summary']['total_passengers'] // dataset['summary']['total_flights']}")
    summary_lines.append("\n" + "=" * 100)
    summary_lines.append("DISRUPTION SUMMARY")
    summary_lines.append("=" * 100)
    for status in sorted(disruption_counts.keys()):
        summary_lines.append(f"{status:20}: {disruption_counts[status]:3} flights")
    summary_lines.append("\n" + "=" * 100)
    summary_lines.append("FLIGHT DETAILS")
    summary_lines.append("=" * 100)
    
    # Sort flights by date and departure time
    sorted_flights = sorted(flights, key=lambda x: x["scheduled_departure"])
    
    current_date = None
    for flight in sorted_flights:
        flight_date_obj = datetime.fromisoformat(flight["scheduled_departure"])
        flight_date_str = flight_date_obj.strftime("%Y-%m-%d")
        
        if current_date != flight_date_str:
            current_date = flight_date_str
            day_label = "TODAY" if flight_date_obj.date() == datetime.now().date() else "TOMORROW"
            summary_lines.append(f"\n📅 {day_label} - {flight_date_str}")
            summary_lines.append("-" * 100)
        
        std = flight_date_obj.strftime("%H:%M")
        sta = datetime.fromisoformat(flight["scheduled_arrival"]).strftime("%H:%M")
        pax_count = flight_passenger_count.get(flight["flight_id"], 0)
        
        # Add disruption indicator
        status_icon = "✅" if flight["disruption_status"] == "On Time" else "⚠️" if flight["disruption_status"] == "Delayed" else "❌" if flight["disruption_status"] == "Cancelled" else "🔄"
        
        base_line = (
            f"{status_icon} {flight['flight_number']:8} | {flight['origin']} → {flight['destination']} | "
            f"Dep: {std} | Arr: {sta} | Aircraft: {flight['aircraft_type']:12} | "
            f"Gate: {flight['gate']:4} | Passengers: {pax_count:3}"
        )
        
        if flight["disruption_status"] != "On Time":
            base_line += f"\n   └─ {flight['disruption_status']}"
            if flight.get("delay_minutes", 0) > 0:
                base_line += f" ({flight['delay_minutes']} min)"
            if flight["disruption_reason"]:
                base_line += f" - {flight['disruption_reason']}"
        
        summary_lines.append(base_line)
    
    summary_lines.append("\n" + "=" * 100)
    summary_lines.append("PASSENGER STATISTICS BY FARE CLASS")
    summary_lines.append("=" * 100)
    
    # Count passengers by fare class
    fare_class_counts = {}
    for passenger in passengers:
        fc = passenger["fare_class"]
        if fc not in fare_class_counts:
            fare_class_counts[fc] = 0
        fare_class_counts[fc] += 1
    
    for fc in sorted(fare_class_counts.keys()):
        summary_lines.append(f"{fc} - {FARE_CLASS_NAMES.get(fc, 'Unknown'):20}: {fare_class_counts[fc]:5} passengers")
    
    summary_lines.append("\n" + "=" * 100)
    
    return "\n".join(summary_lines)

if __name__ == "__main__":
    print("Generating flight and passenger data...")
    dataset = generate_dataset()
    
    # Save flights
    with open("flights_data.json", "w") as f:
        json.dump(dataset["flights"], f, indent=2)
    print(f"✓ Generated {len(dataset['flights'])} flights -> flights_data.json")

    # Save passengers
    with open("passengers_data.json", "w") as f:
        json.dump(dataset["passengers"], f, indent=2)
    print(f"✓ Generated {len(dataset['passengers'])} passengers -> passengers_data.json")

    # Save bookings
    with open("bookings_data.json", "w") as f:
        json.dump(dataset["bookings"], f, indent=2)
    print(f"✓ Generated {len(dataset['bookings'])} bookings -> bookings_data.json")

    # Save disruptions
    with open("disruption_events_data.json", "w") as f:
        json.dump(dataset["disruptions"], f, indent=2)
    print(f"✓ Generated {len(dataset['disruptions'])} disruption events -> disruption_events_data.json")

    # Save resources
    with open("resources_data.json", "w") as f:
        json.dump(dataset["resources"], f, indent=2)
    print(f"✓ Generated {len(dataset['resources'])} resources -> resources_data.json")

    # Save complete dataset
    with open("complete_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"✓ Complete dataset saved -> complete_dataset.json")

    # Generate and save summary
    summary = generate_summary(dataset)
    with open("data_summary.txt", "w") as f:
        f.write(summary)
    print(f"✓ Summary saved -> data_summary.txt")

    # Print summary to console
    print("\n" + summary)
