#!/usr/bin/env python3
"""
Generate new sample airline data:
- all_flights.json: 10-15 flights with complete flight information
- guest_data.json: 300+ passengers per flight
- recommendations with communication suggestions
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# Flight data generation
def generate_flights():
    flights = []
    routes = [
        ("AUH", "LHR", "B777-300ER"),
        ("AUH", "JFK", "A350-900"),
        ("AUH", "SYD", "A380"),
        ("AUH", "BOM", "A350-900"),
        ("AUH", "DXB", "A380"),
        ("AUH", "CDG", "B777-300ER"),
        ("AUH", "FRA", "A350-900"),
        ("AUH", "SIN", "A380"),
        ("AUH", "BKK", "B787-10"),
        ("AUH", "MEL", "B777-300ER"),
        ("AUH", "MAN", "A350-900"),
        ("AUH", "LAX", "B777-300ER"),
        ("AUH", "ICN", "B787-10"),
        ("AUH", "NRT", "B787-9"),
        ("AUH", "IST", "A350-900"),
    ]
    
    disruption_configs = [
        {"flight_idx": 3, "reason": "Aircraft Availability", "delay": 180},
        {"flight_idx": 6, "reason": "Catering Delay", "delay": 120},
        {"flight_idx": 9, "reason": "Crew Unavailable", "delay": 240},
        {"flight_idx": 11, "reason": "Weather Conditions", "delay": 150},
    ]
    
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    for i, (origin, dest, aircraft) in enumerate(routes[:12]):  # Generate 12 flights
        flight_id = str(uuid.uuid4())
        flight_number = f"EY{100 + i*50 + random.randint(1, 49)}"
        scheduled_departure = base_time + timedelta(hours=i*2, days=random.randint(0, 1))
        scheduled_arrival = scheduled_departure + timedelta(hours=random.randint(8, 16))
        
        # Check if this flight has disruption
        disruption = next((d for d in disruption_configs if d["flight_idx"] == i), None)
        
        flight = {
            "flight_id": flight_id,
            "flight_number": flight_number,
            "origin": origin,
            "destination": dest,
            "scheduled_departure": scheduled_departure.isoformat(),
            "scheduled_arrival": scheduled_arrival.isoformat(),
            "estimated_departure": (scheduled_departure + timedelta(minutes=disruption["delay"]) if disruption else scheduled_departure).isoformat(),
            "estimated_arrival": (scheduled_arrival + timedelta(minutes=disruption["delay"]) if disruption else scheduled_arrival).isoformat(),
            "aircraft_type": aircraft,
            "gate": f"{chr(65 + i % 4)}{random.randint(1, 40)}",
            "terminal": str(random.randint(1, 3)),
            "disruption_status": disruption["reason"] if disruption else "On Time",
            "disruption_reason": disruption["reason"] if disruption else None,
            "delay_minutes": disruption["delay"] if disruption else 0,
            "is_disrupted": disruption is not None
        }
        flights.append(flight)
    
    return flights

# Guest/Passenger data generation
def generate_passengers(flights):
    passengers = []
    passenger_id_counter = 1000
    
    first_names = ["John", "Jane", "Ahmed", "Priya", "Maria", "James", "Fatima", "Rajesh", "Elena", "Michael",
                   "Sophia", "Ali", "Aisha", "David", "Emma", "Hassan", "Layla", "Ibrahim", "Zara", "Thomas"]
    last_names = ["Smith", "Johnson", "Khan", "Patel", "Garcia", "Chen", "Al-Mansouri", "Müller", "Fontaine", "Silva"]
    
    loyalty_tiers = ["Guest", "Silver", "Gold", "Platinum"]
    cabin_classes = ["Economy", "Premium Economy", "Business", "First"]
    
    # Generate 300+ passengers per flight
    for flight in flights:
        num_passengers = random.randint(300, 380)
        
        for j in range(num_passengers):
            passenger = {
                "passenger_id": str(passenger_id_counter),
                "flight_id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "pnr": f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))}",
                "email": f"passenger{passenger_id_counter}@example.com",
                "phone": f"+{random.randint(1, 9)}{random.randint(100000000, 999999999)}",
                "loyalty_tier": random.choice(loyalty_tiers),
                "cabin_class": random.choice(cabin_classes),
                "checked_in": random.choice([True, False, True]),
                "has_connection": random.choice([True, False, False, False]),
                "special_service_request": random.choice([None, "Wheelchair", "Unaccompanied Minor", "VVIP", "Pet"]),
                "meal_preference": random.choice(["Regular", "Vegetarian", "Vegan", "Halal", "Kosher"]),
                "seat_number": f"{random.randint(1, 50)}{chr(65 + random.randint(0, 5))}",
                "status": "Booked",
                "recommendation_status": {
                    "rebooked": False,
                    "hotel_voucher_issued": False,
                    "compensation_offered": False,
                    "communication_sent": False
                }
            }
            passengers.append(passenger)
            passenger_id_counter += 1
    
    return passengers

# Generate disruptions
def generate_disruptions(flights):
    disruptions = []
    for flight in flights:
        if flight["is_disrupted"]:
            # Get passengers for this flight
            disruption_id = str(uuid.uuid4())
            affected_count = random.randint(280, 350)
            
            disruption = {
                "disruption_id": disruption_id,
                "flight_id": flight["flight_id"],
                "flight_number": flight["flight_number"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "disruption_type": flight["disruption_reason"],
                "severity": "High" if flight["delay_minutes"] > 200 else "Medium",
                "delay_minutes": flight["delay_minutes"],
                "affected_passenger_count": affected_count,
                "timestamp": datetime.now().isoformat(),
                "resolution_status": "In Progress",
                "estimated_cost": affected_count * (50 + random.randint(10, 100))
            }
            disruptions.append(disruption)
    
    return disruptions

# Generate recommendations with COMMUNICATION suggestions
def generate_recommendations(disruptions):
    recommendations = []
    
    communication_templates = [
        {
            "type": "SMS",
            "priority": "URGENT",
            "content": "Flight {{flight_number}} from {{origin}} to {{destination}} is disrupted. Updates will follow shortly. Reply HELP for assistance.",
            "send_immediately": True
        },
        {
            "type": "Email",
            "priority": "HIGH",
            "content": "Dear Passenger, Your flight {{flight_number}} (Booking {{pnr}}) has experienced a {{disruption_reason}}. Delay: {{delay}} minutes. Our team is working on solutions. Expect rebooked options within 1 hour.",
            "send_immediately": True
        },
        {
            "type": "Phone Call",
            "priority": "URGENT",
            "content": "Courtesy call regarding flight {{flight_number}} disruption. Press 1 for reboking options, 2 for compensation details.",
            "send_immediately": True
        },
        {
            "type": "App Push Notification",
            "priority": "HIGH",
            "content": "Flight disruption alert: {{flight_number}} delayed {{delay}} mins. Check app for rebooking options.",
            "send_immediately": True
        }
    ]
    
    for disruption in disruptions:
        recommendation = {
            "disruption_id": disruption["disruption_id"],
            "flight_number": disruption["flight_number"],
            "recommendation_id": str(uuid.uuid4()),
            "generated_at": datetime.now().isoformat(),
            "priority": "URGENT",
            
            # ===== CRITICAL: INITIAL COMMUNICATIONS =====
            "initial_communications": {
                "send_immediately": True,
                "channels": [
                    {
                        "type": "SMS",
                        "template": communication_templates[0]["content"],
                        "priority": "URGENT",
                        "eta_minutes": 2,
                        "required": True
                    },
                    {
                        "type": "Email",
                        "template": communication_templates[1]["content"],
                        "priority": "HIGH",
                        "eta_minutes": 5,
                        "required": True
                    },
                    {
                        "type": "App Notification",
                        "template": communication_templates[3]["content"],
                        "priority": "HIGH",
                        "eta_minutes": 1,
                        "required": True
                    }
                ],
                "message": f"IMMEDIATE: Send out initial comms to all {disruption['affected_passenger_count']} passengers. Target: < 5 minutes to all channels.",
                "status": "Pending"
            },
            
            # Rebooking options
            "rebooking_options": [
                {
                    "option_id": 1,
                    "flight_number": f"EY{random.randint(100, 999)}",
                    "departure": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "seats_available": random.randint(50, 200),
                    "cabin_upgrade": random.choice([True, False, False])
                },
                {
                    "option_id": 2,
                    "flight_number": f"EY{random.randint(100, 999)}",
                    "departure": (datetime.now() + timedelta(hours=4)).isoformat(),
                    "seats_available": random.randint(100, 300),
                    "cabin_upgrade": False
                }
            ],
            
            # Vouchers and compensation
            "vouchers": [
                {"type": "meal", "amount": 25, "quantity": disruption["affected_passenger_count"]},
                {"type": "hotel", "amount": 150, "quantity": max(1, disruption["affected_passenger_count"] // 2)},
                {"type": "transportation", "amount": 50, "quantity": disruption["affected_passenger_count"] // 3}
            ],
            
            "compensation": [
                {
                    "type": "EU261_cash",
                    "amount": 250 if disruption["delay_minutes"] >= 200 else 125,
                    "eligible_passengers": int(disruption["affected_passenger_count"] * 0.7),
                    "conditions": "Applies to EU/UK departing flights with 3+ hour delay"
                }
            ],
            
            "operational_actions": [
                "Secure standby aircraft from partner airline",
                "Confirm crew availability for rebooked flights",
                "Pre-position ground staff for passenger rebooking"
            ],
            
            "status": "Pending",
            "source": "AI-Recommendation Engine"
        }
        recommendations.append(recommendation)
    
    return recommendations

# Main execution
if __name__ == "__main__":
    print("Generating airline data...")
    
    flights = generate_flights()
    passengers = generate_passengers(flights)
    disruptions = generate_disruptions(flights)
    recommendations = generate_recommendations(disruptions)
    
    # Save all_flights.json
    with open("test_data/all_flights.json", "w") as f:
        json.dump(flights, f, indent=2)
    print(f"✅ Created all_flights.json with {len(flights)} flights")
    
    # Save guest_data.json
    with open("test_data/guest_data.json", "w") as f:
        json.dump(passengers, f, indent=2)
    print(f"✅ Created guest_data.json with {len(passengers)} passengers")
    
    # Save disruptions.json
    with open("test_data/disruptions.json", "w") as f:
        json.dump(disruptions, f, indent=2)
    print(f"✅ Created disruptions.json with {len(disruptions)} disruptions")
    
    # Save recommendations.json
    with open("test_data/recommendations.json", "w") as f:
        json.dump({"recommendations": recommendations}, f, indent=2)
    print(f"✅ Created recommendations.json with {len(recommendations)} recommendations")
    
    # Print summary
    print("\n" + "="*60)
    print("DATA GENERATION SUMMARY")
    print("="*60)
    print(f"Total Flights: {len(flights)}")
    print(f"Total Passengers: {len(passengers)}")
    print(f"Passengers per flight: ~{len(passengers)//len(flights)}")
    print(f"Disrupted flights: {len(disruptions)}")
    print(f"Recommendations generated: {len(recommendations)}")
    print("="*60)
