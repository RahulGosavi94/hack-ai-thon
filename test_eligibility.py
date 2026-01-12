#!/usr/bin/env python3
"""Test eligibility-driven suggestions for different passenger tiers"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

# Sleep to ensure server is ready
time.sleep(2)

def test_passenger_tier(passenger_id, tier_name):
    """Test passenger suggestions for a specific tier"""
    print(f"\n{'='*70}")
    print(f"Testing {tier_name} Tier Passenger: {passenger_id}")
    print(f"{'='*70}")
    
    try:
        response = requests.get(f"{API_BASE}/passenger-suggestions/{passenger_id}")
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
            return
        
        data = response.json()
        
        # Display key information
        print(f"\n✅ Passenger: {data.get('passenger_name')}")
        print(f"   PNR: {data.get('pnr')}")
        print(f"   Flight: {data.get('flight_number')}")
        print(f"   Ticket Class: {data.get('ticket_class')}")
        print(f"   Delay: {data.get('delay_minutes')} minutes")
        print(f"   Priority: {data.get('priority')}")
        
        # Display eligibility
        eligibility = data.get('eligibility', {})
        print(f"\n📋 ELIGIBILITY:")
        print(f"   Eligible Actions: {', '.join(eligibility.get('actions', []))}")
        print(f"   Priority: {eligibility.get('priority')}")
        print(f"   Reason: {eligibility.get('reason')}")
        
        # Display what's available
        print(f"\n🎯 AVAILABLE OPTIONS:")
        
        available_actions = eligibility.get('actions', [])
        
        # Check each action type
        action_types = {
            'meal': 'Meal Vouchers',
            'hotel': 'Hotel Accommodation',
            'rebooking': 'Rebooking Options',
            'compensation': 'Compensation',
            'transport': 'Transport/Connection Assistance'
        }
        
        for action_key, action_label in action_types.items():
            status = "✅ YES" if action_key in available_actions else "❌ NO"
            print(f"   {status} - {action_label}")
        
        # Display AI suggestion
        print(f"\n🤖 AI RECOMMENDATION:")
        if data.get('ai_personalized_note'):
            print(f"   {data.get('ai_personalized_note')}")
        
        # Display summary
        if data.get('summary'):
            print(f"\n📊 SUMMARY:")
            print(f"   Recommended: {data['summary'].get('recommended_action')}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")

# Get all passengers and their tiers
try:
    print("📥 Loading passenger data...")
    with open('test_data/passengers_data.json', 'r') as f:
        passengers = json.load(f)
    
    # Group by tier
    tiers = {}
    for p in passengers:
        tier = p.get('loyalty_tier', 'Guest')
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(p)
    
    # Test one passenger from each tier
    tier_order = ['Platinum', 'Gold', 'Silver', 'Guest']
    tested_tiers = set()
    
    for tier in tier_order:
        if tier in tiers and tier not in tested_tiers:
            passenger = tiers[tier][0]  # Get first passenger of this tier
            pid = passenger.get('id') or passenger.get('passenger_id')
            test_passenger_tier(pid, tier)
            tested_tiers.add(tier)
            time.sleep(1)  # Brief delay between requests
    
    print(f"\n{'='*70}")
    print("✅ Testing complete!")
    print(f"{'='*70}\n")
    
except FileNotFoundError:
    print("❌ Error: passengers_data.json not found")
except Exception as e:
    print(f"❌ Error: {e}")
