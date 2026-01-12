#!/usr/bin/env python3
"""Test eligibility thresholds with different delay scenarios"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_flight_passenger_delay(flight_number):
    """Test passenger suggestions for a flight with specific delay"""
    try:
        # Get flight passengers
        response = requests.get(f"{API_BASE}/flights")
        flights_data = response.json()
        
        # Find flight
        flight = None
        for f in flights_data.get('flights', []):
            if f.get('flight_number') == flight_number:
                flight = f
                break
        
        if not flight:
            print(f"Flight {flight_number} not found")
            return
        
        delay = flight.get('delay_minutes', 0)
        
        # Get passengers for this flight
        response = requests.get(f"{API_BASE}/flights/{flight.get('flight_id')}/passengers")
        passengers = response.json().get('passengers', [])
        
        if not passengers:
            print(f"No passengers found for {flight_number}")
            return
        
        # Test first passenger
        passenger = passengers[0]
        pid = passenger.get('id') or passenger.get('passenger_id')
        
        print(f"\n{'='*70}")
        print(f"Flight {flight_number} - {delay}min delay")
        print(f"{'='*70}")
        print(f"Passenger: {passenger.get('passenger_name')}")
        print(f"Tier: {passenger.get('loyalty_tier')}")
        print(f"Class: {passenger.get('ticket_class')}")
        
        # Get suggestions
        response = requests.get(f"{API_BASE}/passenger-suggestions/{pid}")
        data = response.json()
        
        eligibility = data.get('eligibility', {})
        eligible_actions = eligibility.get('actions', [])
        
        print(f"\n🎯 ELIGIBLE ACTIONS ({len(eligible_actions)} total):")
        
        actions_mapping = {
            'meal': ('Meal', 120),
            'compensation': ('Compensation', 180),
            'rebooking': ('Rebooking', 0),
            'hotel': ('Hotel', 720),
            'transport': ('Transport', 720)
        }
        
        for action_key, (label, threshold) in actions_mapping.items():
            is_eligible = action_key in eligible_actions
            marker = "✅" if is_eligible else "❌"
            threshold_info = f" (threshold: {threshold}min)" if threshold > 0 else " (always)"
            print(f"   {marker} {label}{threshold_info}")
        
        print(f"\nAI Note: {data.get('ai_personalized_note', 'N/A')[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")

# Test different flights with different delays
flights_to_test = [
    'EY129',  # 90 min - should enable: rebooking only
    'EY567',  # 120 min - should enable: rebooking, meal
    'EY234',  # 105 min - should enable: rebooking only
    'EY245',  # 180 min - should enable: rebooking, meal, compensation
]

for flight in flights_to_test:
    test_flight_passenger_delay(flight)
    time.sleep(0.5)

print(f"\n{'='*70}")
print("✅ Eligibility threshold testing complete!")
print(f"{'='*70}\n")
