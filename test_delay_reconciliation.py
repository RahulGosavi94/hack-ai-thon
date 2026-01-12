#!/usr/bin/env python3
"""
Test script to demonstrate delay reconciliation logic (Option 2)
Reconciles delay_minutes from flights_data.json and detected_disruptions.json
by taking the maximum (worst-case) value.
"""

import json
import os

TEST_DATA_DIR = "test_data"

def load_json_file(filename):
    """Load JSON file from test_data directory"""
    filepath = os.path.join(TEST_DATA_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)

def reconcile_delay_minutes(flights_data, disruptions_data, flight_id):
    """
    Reconcile delay_minutes using Option 2: Use worst-case (max)
    delay_minutes = max(
        flights_data['delay_minutes'],
        detected_disruptions['delay_minutes']
    )  # Use worst-case
    """
    # Find flight in flights_data
    flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
    if isinstance(flights_list, dict):
        flights_list = list(flights_list.values())
    
    flight = next((f for f in flights_list if f.get('flight_id') == flight_id or f.get('flight_number') == flight_id), None)
    flights_delay = flight.get('delay_minutes', 0) if flight else 0
    
    # Find disruption in detected_disruptions
    disruptions_list = disruptions_data.get('disruptions', []) if isinstance(disruptions_data, dict) else disruptions_data
    disruption = next((d for d in disruptions_list if d.get('flight_id') == flight_id or d.get('flight_number') == flight_id), None)
    disruptions_delay = disruption.get('delay_minutes', 0) if disruption else 0
    
    # Option 2: Reconcile before use - Use worst-case
    reconciled_delay = max(flights_delay, disruptions_delay)
    
    return {
        'flight_id': flight_id,
        'flights_data_delay': flights_delay,
        'detected_disruptions_delay': disruptions_delay,
        'difference': flights_delay - disruptions_delay,
        'reconciled_delay': reconciled_delay,
        'flight_number': flight.get('flight_number') if flight else disruption.get('flight_number') if disruption else None
    }

if __name__ == "__main__":
    print("="*80)
    print("DELAY RECONCILIATION TEST - Option 2: Use Worst-Case (max)")
    print("="*80)
    print()
    
    # Load data files
    print("Loading data files...")
    flights_data = load_json_file("flights_data.json")
    disruptions_data = load_json_file("detected_disruptions.json")
    print("✓ Data loaded successfully\n")
    
    # Test with EY129 and EY245 as mentioned in the documentation
    test_flights = ["EY129", "EY245"]
    
    for flight_id in test_flights:
        print(f"Testing flight: {flight_id}")
        print("-" * 80)
        
        result = reconcile_delay_minutes(flights_data, disruptions_data, flight_id)
        
        print(f"Flight ID/Number: {result['flight_number']}")
        print(f"flights_data.json delay:        {result['flights_data_delay']} minutes")
        print(f"detected_disruptions.json delay: {result['detected_disruptions_delay']} minutes")
        print(f"Difference:                     {result['difference']:+d} minutes")
        print(f"Reconciled delay (max/worst):   {result['reconciled_delay']} minutes ⭐")
        print()
    
    print("="*80)
    print("Reconciliation complete!")
    print("="*80)
