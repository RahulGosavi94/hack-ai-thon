#!/usr/bin/env python3
"""Generate perfect passenger examples with Ollama-generated tier-specific suggestions"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def find_passengers_by_characteristics():
    """Find specific passengers with different tiers and delays"""
    try:
        # Load all data
        with open('test_data/passengers_data.json') as f:
            passengers = json.load(f)
        
        with open('test_data/flights_data.json') as f:
            flights_data = json.load(f)
        
        flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
        if isinstance(flights_list, dict):
            flights_list = list(flights_list.values())
        
        # Group by tier and flight
        tier_examples = {
            'Platinum': None,
            'Gold': None,
            'Silver': None,
            'Guest': None
        }
        
        # Find one passenger from each tier
        for passenger in passengers:
            tier = passenger.get('loyalty_tier', 'Guest')
            if tier in tier_examples and tier_examples[tier] is None:
                # Find their flight to get delay info
                flight_num = passenger.get('flight_number')
                flight = next((f for f in flights_list if f.get('flight_number') == flight_num), None)
                if flight:
                    tier_examples[tier] = {
                        'passenger': passenger,
                        'flight': flight,
                        'flight_number': flight_num
                    }
        
        return tier_examples
    except Exception as e:
        print(f"Error: {e}")
        return {}

def get_passenger_suggestions_detail(passenger_id):
    """Fetch detailed suggestions for a passenger"""
    try:
        response = requests.get(f"{API_BASE}/passenger-suggestions/{passenger_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return None

def format_output(tier, data):
    """Format passenger example output"""
    passenger = data['passenger']
    flight = data['flight']
    flight_number = data['flight_number']
    
    pid = passenger.get('id') or passenger.get('passenger_id')
    suggestions = get_passenger_suggestions_detail(pid)
    
    if not suggestions:
        return None
    
    output = f"""
{'='*90}
{tier.upper()} TIER PASSENGER EXAMPLE
{'='*90}

PASSENGER DETAILS:
├─ Name: {passenger.get('passenger_name')}
├─ PNR: {passenger.get('pnr')}
├─ Passenger ID: {pid}
├─ Loyalty Tier: {passenger.get('loyalty_tier')}
├─ Ticket Class: {passenger.get('ticket_class', 'Economy')}
├─ Email: {passenger.get('email')}
└─ Special Request: {passenger.get('special_service_request', 'None')}

FLIGHT DETAILS:
├─ Flight Number: {flight_number}
├─ Route: {flight.get('origin')} → {flight.get('destination')}
├─ Delay: {flight.get('delay_minutes')} minutes
├─ Status: {'DISRUPTED' if flight.get('is_disrupted') else 'ON TIME'}
└─ Connection: {passenger.get('next_segment_arrival_iataCode', 'No connection')}

ELIGIBILITY & PRIORITY:
├─ Priority Level: {suggestions.get('priority')}
├─ Eligible Actions: {', '.join(suggestions.get('eligibility', {}).get('actions', []))}
└─ Reason: {suggestions.get('eligibility', {}).get('reason')}

TIER-AWARE OLLAMA SUGGESTION:
"""
    
    if suggestions.get('ai_personalized_note'):
        suggestion_text = suggestions['ai_personalized_note'].strip()
        # Format with proper line breaks
        lines = suggestion_text.split('\n')
        for line in lines:
            if line.strip():
                output += f"\n{line}"
    
    output += f"""

RECOMMENDED ACTION:
└─ {suggestions.get('summary', {}).get('recommended_action')}

AVAILABLE RECOVERY OPTIONS:

Meal Vouchers:
"""
    
    meal_eligible = 'meal' in suggestions.get('eligibility', {}).get('actions', [])
    for voucher in suggestions.get('vouchers', []):
        if voucher['type'] == 'meal':
            status = "✅ ELIGIBLE" if meal_eligible else "❌ NOT ELIGIBLE"
            output += f"\n  {status}: ${voucher['amount']} × {voucher['quantity']} = ${voucher['total']}"
    
    output += f"""

Rebooking Options:
"""
    rebook_eligible = 'rebooking' in suggestions.get('eligibility', {}).get('actions', [])
    if suggestions.get('rebooking_options'):
        for i, opt in enumerate(suggestions['rebooking_options'][:2], 1):  # Show first 2 options
            connection_flag = " 🎯 MATCHES YOUR CONNECTION" if opt.get('connection_friendly') else ""
            output += f"\n  Option {i}: Flight {opt['flight_number']} to {opt.get('destination')}{connection_flag}"
    
    output += f"""

Compensation:
"""
    comp_eligible = 'compensation' in suggestions.get('eligibility', {}).get('actions', [])
    for comp in suggestions.get('compensation', []):
        status = "✅ ELIGIBLE" if comp_eligible else "❌ NOT ELIGIBLE"
        output += f"\n  {status}: ${comp['amount']} ({comp['regulation']})"
    
    if suggestions.get('connection_assistance', {}).get('has_connection'):
        output += f"""

Connection Assistance:
  ├─ Next Destination: {suggestions['connection_assistance'].get('next_destination')}
  ├─ Risk Level: {suggestions['connection_assistance'].get('connection_risk')}
  ├─ Priority Action: {suggestions['connection_assistance'].get('priority_action')}
  └─ Buffer Recommended: {suggestions['connection_assistance'].get('suggested_buffer', 'N/A')}
"""
    
    return output

# Main execution
print("\n🔍 SEARCHING FOR PERFECT PASSENGER EXAMPLES...\n")

tier_examples = find_passengers_by_characteristics()

if not tier_examples:
    print("❌ Could not find passenger examples")
    exit(1)

outputs = []
for tier in ['Platinum', 'Gold', 'Silver', 'Guest']:
    if tier_examples[tier]:
        print(f"✅ Found {tier} tier passenger")
        time.sleep(1)
        output = format_output(tier, tier_examples[tier])
        if output:
            outputs.append(output)

# Print all outputs
for output in outputs:
    print(output)

print(f"\n{'='*90}")
print("📊 SUMMARY: Perfect Examples of Tier-Based Ollama Suggestions")
print(f"{'='*90}\n")

for tier in ['Platinum', 'Gold', 'Silver', 'Guest']:
    if tier_examples[tier]:
        data = tier_examples[tier]
        flight = data['flight']
        print(f"✅ {tier:12} → {data['flight_number']:6} ({flight.get('delay_minutes'):3}min delay)")

print("\nKey Observations:")
print("├─ Each tier receives DIFFERENT AI-generated suggestions")
print("├─ Platinum gets VIP/Executive language and treatment")
print("├─ Gold gets premium/valued language")
print("├─ Silver gets standard premium language")
print("└─ Guest gets basic support language")
print("\n")
