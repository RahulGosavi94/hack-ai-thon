"""
Flask API Server for Airline Disruption Management System
Provides REST API endpoints to fetch flights, disruptions, and trigger LLM recommendations
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Base path for test data
TEST_DATA_DIR = "test_data"

# Cache for loaded data
_data_cache = {}

# ========================
# Aviation Constants & MCT Rules
# ========================
MINIMUM_CONNECTING_TIME = {
    'LHR': 90,  # London Heathrow
    'AUH': 75,  # Abu Dhabi
    'DXB': 90,  # Dubai
    'JFK': 120, # New York
    'CDG': 90,  # Paris
    'LAX': 120, # Los Angeles
    'SFO': 120, # San Francisco
    'BOM': 60,  # Mumbai
    'DEL': 60,  # Delhi
    'CAI': 60,  # Cairo
    'SYD': 120, # Sydney
    'JED': 60,  # Jeddah
    'MAD': 90,  # Madrid
}

DELAY_THRESHOLDS = {
    'short_meal': 120,      # 2 hours = 120 minutes for meal voucher
    'medium_hotel': 720,    # 12 hours = 720 minutes for hotel needed
    'high_compensation': 180  # 3 hours = 180 minutes for compensation eligible
}

def load_json_file(filename):
    """Load JSON file from test_data directory with caching"""
    if filename in _data_cache:
        return _data_cache[filename]
    
    filepath = os.path.join(TEST_DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            _data_cache[filename] = data
            return data
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def is_passenger_disrupted(passenger, flight):
    """
    Determine if a passenger is disrupted.
    A passenger is disrupted if:
    1. They have a connecting flight that will be missed due to delay
    2. OR their arrival delay exceeds SLA threshold
    3. OR their connection time < MCT at connection airport
    """
    delay_minutes = flight.get('delay_minutes', 0)
    
    # Check if passenger has connecting flight
    connecting_flight = passenger.get('connecting_flight')
    connection_airport = passenger.get('next_segment_arrival_iataCode')
    
    if not connecting_flight or not connection_airport:
        # No connection - disrupted only if arrival delay is significant
        return delay_minutes > 60  # More than 1 hour delay
    
    # Calculate if connection will be missed
    mct = MINIMUM_CONNECTING_TIME.get(connection_airport, 90)
    
    # If delay_minutes >= MCT, passenger will miss connection
    return delay_minutes >= mct

def calculate_disruption_eligibility(passenger, flight):
    """
    Calculate what recovery actions a disrupted passenger is eligible for
    Returns: {eligible_for: ['meal', 'hotel', 'rebooking', 'compensation', 'transport'], priority: 'high'|'medium'|'low'}
    """
    eligibility = {
        'eligible_for': [],
        'priority': 'low',
        'reason': '',
        'passenger_id': passenger.get('id') or passenger.get('passenger_id')
    }
    
    if not is_passenger_disrupted(passenger, flight):
        return eligibility
    
    delay_minutes = flight.get('delay_minutes', 0)
    loyalty_tier = passenger.get('loyalty_tier')
    has_ssr = bool(passenger.get('special_service_request'))
    
    # Determine priority
    if loyalty_tier in ['Platinum', 'Gold'] or has_ssr:
        eligibility['priority'] = 'high'
    elif delay_minutes > 180:
        eligibility['priority'] = 'high'
    elif delay_minutes > 120:
        eligibility['priority'] = 'medium'
    else:
        eligibility['priority'] = 'low'
    
    # Determine eligible actions
    if delay_minutes >= DELAY_THRESHOLDS['short_meal']:
        eligibility['eligible_for'].append('meal')
    
    if delay_minutes >= DELAY_THRESHOLDS['high_compensation']:
        eligibility['eligible_for'].append('compensation')
    
    # Rebooking always eligible if disrupted
    if is_passenger_disrupted(passenger, flight):
        eligibility['eligible_for'].append('rebooking')
    
    # Hotel only if next flight is next day
    if delay_minutes >= DELAY_THRESHOLDS['medium_hotel']:
        eligibility['eligible_for'].append('hotel')
        eligibility['eligible_for'].append('transport')
    
    eligibility['reason'] = f"Disrupted passenger: {delay_minutes}min delay, Connection at {passenger.get('next_segment_arrival_iataCode', 'N/A')}"
    
    return eligibility

# ========================
# API ENDPOINTS
# ========================

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the index.html file"""
    return send_file('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

@app.route('/api/flights', methods=['GET'])
def get_all_flights():
    """Get list of all flights with disruption status"""
    try:
        flights_data = load_json_file("flights_data.json")
        disruptions_data = load_json_file("detected_disruptions.json")
        
        # Handle both old and new data formats
        flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
        if isinstance(flights_list, dict):
            flights_list = list(flights_list.values())
        
        flight_list = []
        disrupted_flights = {}
        
        # Extract disrupted flight info by flight_number or flight_id
        if isinstance(disruptions_data, dict) and 'disruptions' in disruptions_data:
            for disruption in disruptions_data['disruptions']:
                flight_num = disruption.get('flight_number')
                flight_id = disruption.get('flight_id')
                disrupted_flights[flight_num] = disruption
                disrupted_flights[flight_id] = disruption
        
        # Build flight list
        for flight in flights_list:
            flight_num = flight.get('flight_number')
            flight_id = flight.get('flight_id')
            disruption = disrupted_flights.get(flight_num) or disrupted_flights.get(flight_id)
            flight_status = flight.get('status', 'On Time')
            # A flight is disrupted if it's in the disruptions data OR if its status indicates a disruption
            is_disrupted = disruption is not None or flight_status in ['Delayed', 'Cancelled', 'Diverted']
            flight_list.append({
                "flight_id": flight.get('flight_id'),
                "flight_number": flight.get('flight_number'),
                "origin": flight.get('origin'),
                "destination": flight.get('destination'),
                "scheduled_departure": flight.get('scheduled_departure'),
                "estimated_departure": flight.get('estimated_departure'),
                "scheduled_arrival": flight.get('scheduled_arrival'),
                "estimated_arrival": flight.get('estimated_arrival'),
                "status": flight_status,
                "disruption_reason": flight.get('disruption_reason'),
                "delay_minutes": flight.get('delay_minutes', 0),
                "aircraft_type": flight.get('aircraft_type'),
                "gate": flight.get('gate'),
                "terminal": flight.get('terminal'),
                "is_disrupted": is_disrupted
            })
        
        return jsonify({"flights": flight_list, "total": len(flight_list)}), 200
    except Exception as e:
        print(f"Error in get_all_flights: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/flights/<flight_id>', methods=['GET'])
def get_flight_details(flight_id):
    """Get detailed information about a specific flight"""
    try:
        flights_data = load_json_file("flights_data.json")
        disruptions_data = load_json_file("detected_disruptions.json")
        passengers_data = load_json_file("passengers_data.json")
        
        # Handle both old and new data formats
        flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
        if isinstance(flights_list, dict):
            flights_list = list(flights_list.values())
        
        # Find flight
        flight = next((f for f in flights_list if f.get('flight_id') == flight_id), None)
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        
        # Find disruption info if exists (match by flight_id or flight_number)
        disruption = None
        flight_number = flight.get('flight_number')
        if isinstance(disruptions_data, dict) and 'disruptions' in disruptions_data:
            disruption = next((d for d in disruptions_data['disruptions'] if d.get('flight_id') == flight_id or d.get('flight_number') == flight_number), None)
        
        # Get passengers for this flight (match by flight_id or flight_number)
        passengers = [p for p in passengers_data if p.get('flight_id') == flight_id or p.get('flight_number') == flight_number]
        
        response = {
            "flight": flight,
            "disruption": disruption,
            "passenger_count": len(passengers),
            "passengers_sample": passengers[:10]  # First 10 passengers as sample
        }
        
        return jsonify(response), 200
    except Exception as e:
        print(f"Error in get_flight_details: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/flights/<flight_id>/passengers', methods=['GET'])
def get_flight_passengers(flight_id):
    """Get all passengers for a specific flight with filters"""
    try:
        passengers_data = load_json_file("passengers_data.json")
        bookings_data = load_json_file("bookings_data.json")
        flights_data = load_json_file("flights_data.json")
        
        # Handle both old and new data formats
        flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
        if isinstance(flights_list, dict):
            flights_list = list(flights_list.values())
        
        # Get query parameters for filtering
        vip_only = request.args.get('vip', 'false').lower() == 'true'
        ssr_only = request.args.get('ssr', 'false').lower() == 'true'
        connections_only = request.args.get('connections', 'false').lower() == 'true'
        
        # Find flight by ID and get flight_number
        flight = next((f for f in flights_list if f.get('flight_id') == flight_id), None)
        flight_number = flight.get('flight_number') if flight else flight_id
        
        # Match passengers by flight_id or flight_number
        passengers = [p for p in passengers_data if p.get('flight_id') == flight_id or p.get('flight_number') == flight_number]
        
        # Apply filters
        if vip_only:
            passengers = [p for p in passengers if p.get('loyalty_tier') in ['Gold', 'Platinum']]
        if ssr_only:
            passengers = [p for p in passengers if p.get('special_service_request')]
        if connections_only:
            # Check if passenger has a connection from booking data
            passengers = [p for p in passengers if any(b.get('pnr') == p.get('pnr') and len(b.get('flight_segments', [])) > 1 for b in bookings_data)]
        
        return jsonify({
            "flight_id": flight_id,
            "passengers": passengers,
            "total": len(passengers)
        }), 200
    except Exception as e:
        print(f"Error in get_flight_passengers: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/disruptions', methods=['GET'])
def get_disruptions():
    """Get all detected disruptions"""
    try:
        disruptions_data = load_json_file("detected_disruptions.json")
        
        if isinstance(disruptions_data, dict) and 'disruptions' in disruptions_data:
            disruptions = disruptions_data['disruptions']
        else:
            disruptions = []
        
        return jsonify({
            "disruptions": disruptions,
            "total": len(disruptions),
            "total_passengers_affected": sum(len(d.get('affected_passenger_list', [])) for d in disruptions)
        }), 200
    except Exception as e:
        print(f"Error in get_disruptions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/disruptions/<disruption_id>/recommendations', methods=['GET'])
def get_recommendations(disruption_id):
    """Get stored recommendations for a disruption"""
    try:
        recommendations_data = load_json_file("recommendations.json")
        
        if isinstance(recommendations_data, dict) and 'recommendations' in recommendations_data:
            rec = next((r for r in recommendations_data['recommendations'] if r.get('disruption_id') == disruption_id), None)
            if rec:
                return jsonify(rec), 200
        
        return jsonify({"error": "Recommendations not found"}), 404
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/manager-summary', methods=['GET'])
def get_manager_summary():
    """Get manager summary: costs, impacts, and statistics"""
    try:
        disruptions_data = load_json_file("detected_disruptions.json")
        recommendations_data = load_json_file("recommendations.json")
        
        total_passengers_affected = 0
        total_cost = 0
        hotel_rooms_needed = 0
        meal_vouchers_issued = 0
        passengers_reprotected = 0
        total_voucher_value = 0
        
        if isinstance(disruptions_data, dict) and 'disruptions' in disruptions_data:
            total_passengers_affected = sum(len(d.get('affected_passenger_list', [])) for d in disruptions_data['disruptions'])
            total_cost = disruptions_data.get('total_estimated_cost', 0)
        
        # Count mass actions: meal coupons issued
        try:
            if os.path.exists(os.path.join(TEST_DATA_DIR, "meal_coupons.json")):
                meal_coupons = load_json_file("meal_coupons.json")
                if isinstance(meal_coupons, list):
                    meal_vouchers_issued = len(meal_coupons)
                    total_voucher_value += sum(c.get('total_value', 0) for c in meal_coupons)
        except:
            pass
        
        # Count mass actions: rebookings processed
        try:
            if os.path.exists(os.path.join(TEST_DATA_DIR, "rebookings.json")):
                rebookings = load_json_file("rebookings.json")
                if isinstance(rebookings, list):
                    passengers_reprotected = len([r for r in rebookings if r.get('status') == 'Confirmed'])
        except:
            pass
        
        # Add hotel costs from recommendations (estimate $200 per night)
        if isinstance(recommendations_data, dict) and 'recommendations' in recommendations_data:
            for rec in recommendations_data['recommendations']:
                # Count vouchers from recommendations
                vouchers = rec.get('vouchers', [])
                if isinstance(vouchers, list):
                    for v in vouchers:
                        if v.get('type') == 'hotel':
                            hotel_rooms_needed += 1
                            total_voucher_value += v.get('amount', 200)
        
        return jsonify({
            "total_passengers_affected": total_passengers_affected,
            "total_cost_impact": total_cost,
            "hotel_rooms_needed": hotel_rooms_needed,
            "vouchers_issued": meal_vouchers_issued,
            "passengers_reprotected": passengers_reprotected,
            "total_voucher_value": total_voucher_value,
            "average_cost_per_passenger": total_cost / total_passengers_affected if total_passengers_affected > 0 else 0
        }), 200
    except Exception as e:
        print(f"Error in get_manager_summary: {e}")
        return jsonify({"error": str(e)}), 500

def query_ollama_for_passenger(passenger, flight, delay_minutes):
    """Query Ollama to generate unique suggestions for a specific passenger"""
    import requests
    
    # Determine loyalty tier and service level
    loyalty_tier = passenger.get('loyalty_tier', 'Guest')
    ticket_class = passenger.get('ticket_class', passenger.get('fare_class_name', 'Economy'))
    ssr = passenger.get('special_service_request')
    next_dest = passenger.get('next_segment_arrival_iataCode', 'None')
    
    # Build tier-specific context
    tier_benefits = ""
    if loyalty_tier in ['Platinum', 'Gold']:
        tier_benefits = f"This {loyalty_tier} tier passenger should receive: executive lounge access, priority rebooking, concierge service, complimentary upgrades."
        service_level = "VIP/Executive"
    elif loyalty_tier == 'Silver':
        tier_benefits = "This Silver tier passenger should receive: lounge access, standard priority rebooking, meal vouchers."
        service_level = "Premium"
    else:
        tier_benefits = "This standard tier passenger should receive: standard rebooking, meal vouchers, compensation per regulations."
        service_level = "Standard"
    
    # Build class-specific compensation
    class_compensation = ""
    if ticket_class in ['First', 'Business']:
        class_compensation = "As a premium cabin passenger, offer suite upgrades, premium hotel options, or cash compensation at higher tier."
    else:
        class_compensation = "As an economy/premium economy passenger, standard compensation and meal vouchers apply."
    
    # Build special needs context
    special_needs = ""
    if ssr:
        special_needs = f"IMPORTANT: Passenger has special service requirement ({ssr}) - ensure dedicated assistance and priority handling."
    
    # Build connection context
    connection_context = ""
    if next_dest and next_dest != 'None':
        connection_context = f"Passenger has tight connection to {next_dest}. Prioritize rebooking to preserve connection. If connection cannot be guaranteed, offer alternative routing."
    else:
        connection_context = "Passenger has no onward connection - focus on comfort and compensation."
    
    prompt = f"""You are an airline disruption manager providing personalized service recovery. Generate a unique, tailored recommendation.

PASSENGER PROFILE:
- Name: {passenger.get('passenger_name', 'Unknown')}
- Loyalty Status: {loyalty_tier} ({service_level} Service Level)
- Ticket Class: {ticket_class}
- Flight: {flight.get('flight_number')} ({flight.get('origin')} → {flight.get('destination')})
- Delay: {delay_minutes} minutes
- Next Connection: {next_dest}

SERVICE GUIDELINES:
{tier_benefits}
{class_compensation}
{special_needs if special_needs else ''}
{connection_context}

Generate a PERSONALIZED recommendation (2-3 sentences) that:
1. Reflects their loyalty tier and service level
2. Offers tier-appropriate solutions (mention specific benefits like lounge, concierge, upgrades for high tiers)
3. Addresses their specific situation (connection, special needs, etc.)
4. Provides concrete next steps

IMPORTANT: Make it DIFFERENT for each tier. Platinum/Gold get executive treatment, Silver gets standard premium, others get basic + compensation.

Keep response under 120 words and make it sound personal and empathetic."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.8, "num_predict": 180}
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Ollama error: {e}")
    
    return None

@app.route('/api/recommendations/generate', methods=['POST'])
def generate_recommendations():
    """Trigger LLM to generate recommendations for a disruption"""
    try:
        data = request.get_json()
        flight_id = data.get('flight_id')
        
        if not flight_id:
            return jsonify({"error": "flight_id required"}), 400
        
        # Return pre-computed recommendations (LLM integration optional)
        recommendations_data = load_json_file("recommendations.json")
        
        return jsonify({
            "status": "success",
            "message": "Recommendations loaded",
            "recommendations": recommendations_data.get('recommendations', [])
        }), 200
    except Exception as e:
        print(f"Error in generate_recommendations: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/passenger-suggestions/<passenger_id>', methods=['GET'])
def get_passenger_suggestions(passenger_id):
    """Generate AI suggestions tailored for a specific passenger"""
    try:
        # Load all required data
        passengers_data = load_json_file("passengers_data.json")
        passenger = next((p for p in passengers_data if p.get('id') == passenger_id or p.get('passenger_id') == passenger_id), None)
        
        if not passenger:
            return jsonify({"error": "Passenger not found"}), 404
        
        flights_data = load_json_file("flights_data.json")
        recommendations_data = load_json_file("recommendations.json")
        
        # Handle both old and new data formats
        flights_list = flights_data.get('flights', flights_data) if isinstance(flights_data, dict) else flights_data
        if isinstance(flights_list, dict):
            flights_list = list(flights_list.values())
        
        flight_number = passenger.get('flight_number')
        disruption_id = f"DISR_{flight_number}"
        
        # Get flight and recommendations
        flight = next((f for f in flights_list if f.get('flight_number') == flight_number), None)
        rec = next((r for r in recommendations_data.get('recommendations', []) if r.get('disruption_id') == disruption_id), None)
        
        if not rec or not flight:
            return jsonify({"error": "Recommendations or flight not found"}), 404
        
        # Get passenger's next destination
        next_destination = passenger.get('next_segment_arrival_iataCode', 'AUH')
        current_origin = flight.get('origin', 'AUH')
        ticket_class = passenger.get('ticket_class', passenger.get('fare_class_name', 'Economy'))
        passenger_name = passenger.get('passenger_name', passenger.get('full_name', 'Passenger'))
        delay_minutes = flight.get('delay_minutes', 60)
        
        # Calculate wait time and priority
        wait_hours = delay_minutes / 60
        priority = "CRITICAL" if wait_hours > 4 else "HIGH" if wait_hours > 2 else "NORMAL"
        
        # Filter rebooking options relevant to passenger's next destination
        enhanced_rebooking = []
        for opt in rec.get('rebooking_options', []):
            rebook_flight = next((f for f in flights_list if f.get('flight_number') == opt.get('flight_number')), None)
            if rebook_flight:
                # Check if flight goes to or near passenger's next destination
                flight_destination = rebook_flight.get('destination')
                
                # Create personalized rebooking option
                enhanced_opt = {
                    "option_id": opt.get('option_id'),
                    "flight_number": opt.get('flight_number'),
                    "departure": rebook_flight.get('estimated_departure') or rebook_flight.get('scheduled_departure'),
                    "arrival": rebook_flight.get('estimated_arrival') or rebook_flight.get('scheduled_arrival'),
                    "origin": rebook_flight.get('origin'),
                    "destination": rebook_flight.get('destination'),
                    "seats_available": opt.get('seats_available', 0),
                    "cabin_class": ticket_class,
                    "cabin_upgrade": ticket_class in ['First', 'Business'],
                    "aircraft_type": rebook_flight.get('aircraft_type'),
                    "connection_friendly": flight_destination == next_destination.split(',')[0] if next_destination else False
                }
                enhanced_rebooking.append(enhanced_opt)
        
        # Personalize vouchers based on ticket class and wait time
        vouchers = []
        base_meal = 25 if ticket_class == 'Economy' else 40 if ticket_class == 'Business' else 75
        base_hotel = 150 if ticket_class == 'Economy' else 200 if ticket_class == 'Business' else 300
        
        if wait_hours > 1:
            vouchers.append({
                "type": "meal",
                "amount": base_meal,
                "quantity": 1 + int(wait_hours / 4),  # More meals for longer delays
                "total": base_meal * (1 + int(wait_hours / 4))
            })
        
        if wait_hours > 3:
            vouchers.append({
                "type": "hotel",
                "amount": base_hotel,
                "quantity": 1,
                "total": base_hotel
            })
        
        vouchers.append({
            "type": "transportation",
            "amount": 50,
            "quantity": 1,
            "total": 50
        })
        
        # Personalize compensation based on ticket class and regulations
        compensation_amount = 125 if ticket_class == 'Economy' else 250 if ticket_class == 'Business' else 400
        
        # Generate personalized communication templates
        communication_channels = [
            {
                "type": "Email",
                "template": f"Dear {passenger_name}, We sincerely apologize for the delay on your flight {flight_number}. Your new estimated departure is in {int(delay_minutes)} minutes. We've ensured a {ticket_class} seat on an alternative flight if needed. Your next destination {next_destination} is our priority. Please confirm your preference within 30 minutes.",
                "priority": priority,
                "eta_minutes": 2,
                "required": True
            },
            {
                "type": "SMS",
                "template": f"Flight {flight_number} delayed {int(delay_minutes)} mins. {passenger_name}, we're prioritizing your connection to {next_destination}. Check email for rebooking options.",
                "priority": "URGENT",
                "eta_minutes": 1,
                "required": True
            },
            {
                "type": "App Notification",
                "template": f"Flight delayed. New options available for your {next_destination} connection. Click to review rebooking offers.",
                "priority": "HIGH",
                "eta_minutes": 1,
                "required": True
            }
        ]
        
        # If passenger has connection, add connection-specific notification
        if next_destination and next_destination != 'N/A':
            communication_channels.append({
                "type": "Special Alert",
                "template": f"PRIORITY: Connection to {next_destination} may be at risk. We're securing a backup flight for you automatically.",
                "priority": "CRITICAL",
                "eta_minutes": 1,
                "required": True
            })
        
        # Build final suggestions
        passenger_suggestions = {
            "passenger_id": passenger_id,
            "passenger_name": passenger_name,
            "flight_number": flight_number,
            "pnr": passenger.get('pnr'),
            "email": passenger.get('email'),
            "ticket_class": ticket_class,
            "priority": priority,
            "vip_status": passenger.get('vip_status'),
            "delay_minutes": delay_minutes,
            "next_destination": next_destination if next_destination and next_destination != 'N/A' else None,
            
            # Personalized communications
            "communications": {
                "send_immediately": True,
                "channels": communication_channels,
                "message": f"PRIORITY {priority}: Notify {passenger_name} about {delay_minutes}min delay and {next_destination} connection risk"
            },
            
            # Personalized rebooking options
            "rebooking_options": enhanced_rebooking,
            
            # Personalized vouchers
            "vouchers": vouchers,
            
            # Personalized compensation
            "compensation": [
                {
                    "type": "delay_compensation",
                    "amount": compensation_amount,
                    "eligible": True,
                    "reason": f"{ticket_class} class: Flight delayed {int(delay_minutes)} minutes (EU261)",
                    "regulation": "EU261",
                    "ticket_class_multiplier": 1 if ticket_class == 'Economy' else 2 if ticket_class == 'Business' else 3.2
                }
            ],
            
            # Connection assistance
            "connection_assistance": {
                "has_connection": bool(next_destination and next_destination != 'N/A'),
                "next_destination": next_destination if next_destination and next_destination != 'N/A' else None,
                "connection_risk": "HIGH" if delay_minutes > 120 else "MEDIUM" if delay_minutes > 60 else "LOW",
                "priority_action": f"Secure {next_destination} connection" if next_destination and next_destination != 'N/A' else "No connection needed",
                "suggested_buffer": f"Minimum 2 hour layover recommended for {next_destination}" if next_destination else None
            },
            
            # Summary for agent
            "summary": {
                "passenger_priority": priority,
                "reason": f"{passenger_name} ({ticket_class}): {delay_minutes}min delay, connection to {next_destination}",
                "recommended_action": "PRIORITIZE: Offer cabin upgrade + priority rebooking for connection" if ticket_class != 'First' else "Offer premium concierge service"
            }
        }
        
        # Add Ollama-generated personalized recommendation
        ollama_recommendation = query_ollama_for_passenger(passenger, flight, delay_minutes)
        if ollama_recommendation:
            passenger_suggestions["ai_personalized_note"] = ollama_recommendation
            passenger_suggestions["ai_generated"] = True
        else:
            passenger_suggestions["ai_generated"] = False
        
        # Calculate and add eligibility data (actions available for this passenger)
        eligibility = calculate_disruption_eligibility(passenger, flight)
        passenger_suggestions["eligibility"] = {
            "actions": eligibility.get("eligible_for", []),
            "priority": eligibility.get("priority", "normal"),
            "reason": eligibility.get("reason", "")
        }
        
        return jsonify(passenger_suggestions), 200
    except Exception as e:
        print(f"Error in get_passenger_suggestions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/apply-plan', methods=['POST'])
def apply_plan():
    """Simulate applying a passenger plan"""
    try:
        data = request.get_json()
        passenger_id = data.get('passenger_id')
        action = data.get('action')
        
        return jsonify({
            "status": "success",
            "message": f"Action '{action}' applied for passenger {passenger_id}",
            "simulated": True
        }), 200
    except Exception as e:
        print(f"Error in apply_plan: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/save-meal-coupon', methods=['POST'])
def save_meal_coupon():
    """Save meal coupon issuance record"""
    try:
        from datetime import datetime
        import uuid
        
        data = request.get_json()
        
        # Create unique action record
        meal_coupon = {
            "id": str(uuid.uuid4()),
            "action_id": "MC_" + str(uuid.uuid4())[:8].upper(),
            "passenger_id": data.get('passenger_id'),
            "passenger_name": data.get('passenger_name'),
            "pnr": data.get('pnr'),
            "email": data.get('email'),
            "flight_number": data.get('flight_number'),
            "coupon_amount": data.get('amount'),
            "quantity": data.get('quantity', 1),
            "total_value": data.get('total_value'),
            "notes": data.get('notes', ''),
            "issued_by": data.get('issued_by', 'System'),
            "issued_date": datetime.now().isoformat(),
            "status": "Issued",
            "validity_days": 90
        }
        
        # Load existing coupons or create new
        meal_coupons = load_json_file("meal_coupons.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "meal_coupons.json")) else []
        if not isinstance(meal_coupons, list):
            meal_coupons = []
        
        meal_coupons.append(meal_coupon)
        
        # Save to file
        filepath = os.path.join(TEST_DATA_DIR, "meal_coupons.json")
        with open(filepath, 'w') as f:
            json.dump(meal_coupons, f, indent=2)
        
        # Clear cache
        if "meal_coupons.json" in _data_cache:
            del _data_cache["meal_coupons.json"]
        
        return jsonify({
            "status": "success",
            "message": "Meal coupon saved",
            "action_id": meal_coupon['action_id'],
            "data": meal_coupon
        }), 200
    except Exception as e:
        print(f"Error in save_meal_coupon: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/save-hotel-voucher', methods=['POST'])
def save_hotel_voucher():
    """Save hotel voucher issuance record"""
    try:
        from datetime import datetime
        import uuid
        
        data = request.get_json()
        
        hotel_voucher = {
            "id": str(uuid.uuid4()),
            "action_id": "HV_" + str(uuid.uuid4())[:8].upper(),
            "passenger_id": data.get('passenger_id'),
            "passenger_name": data.get('passenger_name'),
            "pnr": data.get('pnr'),
            "email": data.get('email'),
            "flight_number": data.get('flight_number'),
            "hotel_amount": data.get('amount'),
            "quantity": data.get('quantity', 1),
            "total_value": data.get('total_value'),
            "hotel_category": data.get('hotel_category', 'Standard'),
            "check_in_date": data.get('check_in_date'),
            "nights": data.get('nights', 1),
            "notes": data.get('notes', ''),
            "issued_by": data.get('issued_by', 'System'),
            "issued_date": datetime.now().isoformat(),
            "status": "Issued",
            "validity_days": 90
        }
        
        hotel_vouchers = load_json_file("hotel_vouchers.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "hotel_vouchers.json")) else []
        if not isinstance(hotel_vouchers, list):
            hotel_vouchers = []
        
        hotel_vouchers.append(hotel_voucher)
        
        filepath = os.path.join(TEST_DATA_DIR, "hotel_vouchers.json")
        with open(filepath, 'w') as f:
            json.dump(hotel_vouchers, f, indent=2)
        
        if "hotel_vouchers.json" in _data_cache:
            del _data_cache["hotel_vouchers.json"]
        
        return jsonify({
            "status": "success",
            "message": "Hotel voucher saved",
            "action_id": hotel_voucher['action_id'],
            "data": hotel_voucher
        }), 200
    except Exception as e:
        print(f"Error in save_hotel_voucher: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/save-compensation', methods=['POST'])
def save_compensation():
    """Save compensation payment record"""
    try:
        from datetime import datetime
        import uuid
        
        data = request.get_json()
        
        compensation = {
            "id": str(uuid.uuid4()),
            "action_id": "COMP_" + str(uuid.uuid4())[:8].upper(),
            "passenger_id": data.get('passenger_id'),
            "passenger_name": data.get('passenger_name'),
            "pnr": data.get('pnr'),
            "email": data.get('email'),
            "flight_number": data.get('flight_number'),
            "amount": data.get('amount'),
            "currency": data.get('currency', 'USD'),
            "reason": data.get('reason'),
            "regulation": data.get('regulation', 'EU261'),
            "delay_minutes": data.get('delay_minutes'),
            "payment_method": data.get('payment_method', 'Cash/Card'),
            "notes": data.get('notes', ''),
            "approved_by": data.get('approved_by', 'System'),
            "approved_date": datetime.now().isoformat(),
            "status": "Approved",
            "payment_status": "Pending"
        }
        
        compensations = load_json_file("compensations.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "compensations.json")) else []
        if not isinstance(compensations, list):
            compensations = []
        
        compensations.append(compensation)
        
        filepath = os.path.join(TEST_DATA_DIR, "compensations.json")
        with open(filepath, 'w') as f:
            json.dump(compensations, f, indent=2)
        
        if "compensations.json" in _data_cache:
            del _data_cache["compensations.json"]
        
        return jsonify({
            "status": "success",
            "message": "Compensation saved",
            "action_id": compensation['action_id'],
            "data": compensation
        }), 200
    except Exception as e:
        print(f"Error in save_compensation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/save-rebooking', methods=['POST'])
def save_rebooking():
    """Save rebooking record"""
    try:
        from datetime import datetime
        import uuid
        
        data = request.get_json()
        
        rebooking = {
            "id": str(uuid.uuid4()),
            "action_id": "RBK_" + str(uuid.uuid4())[:8].upper(),
            "passenger_id": data.get('passenger_id'),
            "passenger_name": data.get('passenger_name'),
            "pnr": data.get('pnr'),
            "email": data.get('email'),
            "original_flight": data.get('original_flight'),
            "new_flight": data.get('new_flight'),
            "new_departure": data.get('new_departure'),
            "new_arrival": data.get('new_arrival'),
            "seat_number": data.get('seat_number'),
            "cabin_class": data.get('cabin_class'),
            "cabin_upgrade": data.get('cabin_upgrade', False),
            "notes": data.get('notes', ''),
            "approved_by": data.get('approved_by', 'System'),
            "approved_date": datetime.now().isoformat(),
            "status": "Booked",
            "confirmation_sent": False
        }
        
        rebookings = load_json_file("rebookings.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "rebookings.json")) else []
        if not isinstance(rebookings, list):
            rebookings = []
        
        rebookings.append(rebooking)
        
        filepath = os.path.join(TEST_DATA_DIR, "rebookings.json")
        with open(filepath, 'w') as f:
            json.dump(rebookings, f, indent=2)
        
        if "rebookings.json" in _data_cache:
            del _data_cache["rebookings.json"]
        
        return jsonify({
            "status": "success",
            "message": "Rebooking saved",
            "action_id": rebooking['action_id'],
            "data": rebooking
        }), 200
    except Exception as e:
        print(f"Error in save_rebooking: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/save-message', methods=['POST'])
def save_message():
    """Save sent message record"""
    try:
        from datetime import datetime
        import uuid
        
        data = request.get_json()
        
        message = {
            "id": str(uuid.uuid4()),
            "action_id": "MSG_" + str(uuid.uuid4())[:8].upper(),
            "passenger_id": data.get('passenger_id'),
            "passenger_name": data.get('passenger_name'),
            "pnr": data.get('pnr'),
            "email": data.get('email'),
            "flight_number": data.get('flight_number'),
            "message_type": data.get('message_type', 'Email'),
            "recipient": data.get('recipient'),
            "subject": data.get('subject', ''),
            "message_body": data.get('message_body'),
            "sent_by": data.get('sent_by', 'System'),
            "sent_date": datetime.now().isoformat(),
            "status": "Sent",
            "read_receipt": False
        }
        
        messages = load_json_file("sent_messages.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "sent_messages.json")) else []
        if not isinstance(messages, list):
            messages = []
        
        messages.append(message)
        
        filepath = os.path.join(TEST_DATA_DIR, "sent_messages.json")
        with open(filepath, 'w') as f:
            json.dump(messages, f, indent=2)
        
        if "sent_messages.json" in _data_cache:
            del _data_cache["sent_messages.json"]
        
        return jsonify({
            "status": "success",
            "message": "Message saved",
            "action_id": message['action_id'],
            "data": message
        }), 200
    except Exception as e:
        print(f"Error in save_message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/approve-execute', methods=['POST'])
def approve_execute():
    """Simulate approving and executing all recommendations"""
    try:
        return jsonify({
            "status": "success",
            "message": "All recommendations approved and executed",
            "simulated": True,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        print(f"Error in approve_execute: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/available-flights/<destination>', methods=['GET'])
def get_available_flights(destination):
    """Get available flights for a given destination"""
    try:
        available_flights_data = load_json_file("available_flights.json")
        
        if destination in available_flights_data:
            flights = available_flights_data[destination]
            return jsonify({
                "destination": destination,
                "flights": flights,
                "total": len(flights)
            }), 200
        else:
            return jsonify({
                "destination": destination,
                "flights": [],
                "total": 0
            }), 200
    except Exception as e:
        print(f"Error in get_available_flights: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/passenger/<passenger_id>/send-message', methods=['POST'])
def send_passenger_message(passenger_id):
    """Send message to passenger and track it"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Load message tracking
        messages_data = load_json_file("passenger_messages.json")
        
        if passenger_id in messages_data:
            messages_data[passenger_id]['messages_sent'].append({
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "status": "sent"
            })
            
            # Save updated data
            filepath = os.path.join(TEST_DATA_DIR, "passenger_messages.json")
            with open(filepath, 'w') as f:
                json.dump(messages_data, f, indent=2)
            
            # Clear from cache to reload on next access
            if "passenger_messages.json" in _data_cache:
                del _data_cache["passenger_messages.json"]
            
            return jsonify({
                "status": "success",
                "message": "Message sent successfully",
                "passenger_id": passenger_id
            }), 200
        else:
            return jsonify({"error": "Passenger not found"}), 404
    except Exception as e:
        print(f"Error in send_passenger_message: {e}")
        return jsonify({"error": str(e)}), 500

# ========================
# Error Handlers
# ========================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ========================
# Mass Action Endpoints
# ========================

@app.route('/api/actions/mass-meal-coupons', methods=['POST'])
def mass_meal_coupons():
    """Issue meal coupons to multiple passengers at once"""
    try:
        data = request.json
        passenger_ids = data.get('passenger_ids', [])
        amount = data.get('amount', 25)
        quantity = data.get('quantity', 1)
        
        if not passenger_ids:
            return jsonify({"error": "No passengers selected"}), 400
        
        # Load all passengers to get their details
        passengers_data = load_json_file("passengers_data.json")
        
        meal_coupons = load_json_file("meal_coupons.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "meal_coupons.json")) else []
        if not isinstance(meal_coupons, list):
            meal_coupons = []
        
        issued_coupons = []
        
        for passenger_id in passenger_ids:
            # Find passenger details
            passenger = next((p for p in passengers_data if p.get('id') == passenger_id or p.get('passenger_id') == passenger_id), None)
            
            if passenger:
                coupon = {
                    "id": str(uuid.uuid4()),
                    "coupon_id": "MC_" + str(uuid.uuid4())[:8].upper(),
                    "passenger_id": passenger_id,
                    "passenger_name": passenger.get('full_name') or passenger.get('passenger_name'),
                    "pnr": passenger.get('pnr'),
                    "email": passenger.get('email'),
                    "flight_number": passenger.get('flight_number'),
                    "amount": amount,
                    "quantity": quantity,
                    "total_value": amount * quantity,
                    "issued_by": "Mass Action",
                    "issued_date": datetime.now().isoformat(),
                    "status": "Issued",
                    "validity_days": 30
                }
                
                meal_coupons.append(coupon)
                issued_coupons.append(coupon)
        
        # Save updated meal coupons
        filepath = os.path.join(TEST_DATA_DIR, "meal_coupons.json")
        with open(filepath, 'w') as f:
            json.dump(meal_coupons, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"Issued meal coupons to {len(issued_coupons)} passengers",
            "coupons": issued_coupons
        }), 200
        
    except Exception as e:
        print(f"Error in mass_meal_coupons: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/actions/mass-rebookings', methods=['POST'])
def mass_rebookings():
    """Rebook multiple passengers to a new flight"""
    try:
        data = request.json
        passenger_ids = data.get('passenger_ids', [])
        new_flight_number = data.get('new_flight_number')
        new_departure_time = data.get('new_departure_time')
        
        if not passenger_ids:
            return jsonify({"error": "No passengers selected"}), 400
        
        if not new_flight_number:
            return jsonify({"error": "No alternative flight selected"}), 400
        
        # Load all passengers to get their details
        passengers_data = load_json_file("passengers_data.json")
        
        rebookings = load_json_file("rebookings.json") if os.path.exists(os.path.join(TEST_DATA_DIR, "rebookings.json")) else []
        if not isinstance(rebookings, list):
            rebookings = []
        
        processed_rebookings = []
        
        for passenger_id in passenger_ids:
            # Find passenger details
            passenger = next((p for p in passengers_data if p.get('id') == passenger_id or p.get('passenger_id') == passenger_id), None)
            
            if passenger:
                rebooking = {
                    "id": str(uuid.uuid4()),
                    "rebooking_id": "RBK_" + str(uuid.uuid4())[:8].upper(),
                    "passenger_id": passenger_id,
                    "passenger_name": passenger.get('full_name') or passenger.get('passenger_name'),
                    "pnr": passenger.get('pnr'),
                    "email": passenger.get('email'),
                    "original_flight": passenger.get('flight_number'),
                    "new_flight_number": new_flight_number,
                    "new_departure_time": new_departure_time,
                    "rebooking_type": "Mass Rebooking",
                    "processed_by": "Mass Action",
                    "processed_date": datetime.now().isoformat(),
                    "status": "Confirmed",
                    "confirmation_sent": True
                }
                
                rebookings.append(rebooking)
                processed_rebookings.append(rebooking)
        
        # Save updated rebookings
        filepath = os.path.join(TEST_DATA_DIR, "rebookings.json")
        with open(filepath, 'w') as f:
            json.dump(rebookings, f, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"Rebooked {len(processed_rebookings)} passengers to {new_flight_number}",
            "rebookings": processed_rebookings
        }), 200
        
    except Exception as e:
        print(f"Error in mass_rebookings: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/flights/<flight_id>/disrupted-passengers', methods=['GET'])
def get_disrupted_passengers(flight_id):
    """
    Get only disrupted passengers for a flight.
    Filters passengers based on disruption eligibility rules.
    """
    try:
        # Get flight
        flights_data = load_json_file("flights_data.json")
        flight = next((f for f in flights_data['flights'] if f['flight_id'] == flight_id), None)
        
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        
        # Get all passengers for flight
        passengers_data = load_json_file("passengers_data.json")
        flight_passengers = [p for p in passengers_data if p.get('flight_number') == flight.get('flight_number')]
        
        # Filter for disrupted passengers only
        disrupted = []
        for passenger in flight_passengers:
            if is_passenger_disrupted(passenger, flight):
                eligibility = calculate_disruption_eligibility(passenger, flight)
                passenger['disruption_info'] = eligibility
                disrupted.append(passenger)
        
        return jsonify({
            "flight_id": flight_id,
            "flight_number": flight.get('flight_number'),
            "total_passengers": len(flight_passengers),
            "disrupted_passengers": len(disrupted),
            "passengers": disrupted,
            "disruption_details": {
                "delay_minutes": flight.get('delay_minutes'),
                "reason": flight.get('disruption_reason'),
                "is_disrupted": flight.get('is_disrupted')
            }
        }), 200
        
    except Exception as e:
        print(f"Error in get_disrupted_passengers: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/disruption-analysis', methods=['GET'])
def get_disruption_analysis():
    """
    Real-time disruption analysis:
    - All disrupted flights
    - Affected passengers count
    - Recovery actions needed
    - Estimated costs
    """
    try:
        flights_data = load_json_file("flights_data.json")
        passengers_data = load_json_file("passengers_data.json")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "disrupted_flights": [],
            "total_disrupted_passengers": 0,
            "recovery_actions_needed": {
                "meal": 0,
                "rebooking": 0,
                "hotel": 0,
                "compensation": 0
            },
            "estimated_total_cost": 0
        }
        
        for flight in flights_data['flights']:
            if not flight.get('is_disrupted'):
                continue
            
            flight_passengers = [p for p in passengers_data if p.get('flight_number') == flight.get('flight_number')]
            disrupted_passengers = [p for p in flight_passengers if is_passenger_disrupted(p, flight)]
            
            if not disrupted_passengers:
                continue
            
            flight_analysis = {
                "flight_number": flight.get('flight_number'),
                "origin": flight.get('origin'),
                "destination": flight.get('destination'),
                "delay_minutes": flight.get('delay_minutes'),
                "disruption_reason": flight.get('disruption_reason'),
                "disrupted_passengers_count": len(disrupted_passengers),
                "recovery_actions": {
                    "meal": 0,
                    "rebooking": 0,
                    "hotel": 0,
                    "compensation": 0
                },
                "estimated_cost": 0
            }
            
            # Calculate actions needed per passenger
            for passenger in disrupted_passengers:
                eligibility = calculate_disruption_eligibility(passenger, flight)
                
                for action in eligibility['eligible_for']:
                    flight_analysis['recovery_actions'][action] += 1
                    analysis['recovery_actions_needed'][action] += 1
                
                # Rough cost estimation
                if 'meal' in eligibility['eligible_for']:
                    flight_analysis['estimated_cost'] += 25
                if 'rebooking' in eligibility['eligible_for']:
                    flight_analysis['estimated_cost'] += 50
                if 'hotel' in eligibility['eligible_for']:
                    flight_analysis['estimated_cost'] += 150
                if 'compensation' in eligibility['eligible_for']:
                    flight_analysis['estimated_cost'] += 250
            
            analysis['total_disrupted_passengers'] += len(disrupted_passengers)
            analysis['estimated_total_cost'] += flight_analysis['estimated_cost']
            analysis['disrupted_flights'].append(flight_analysis)
        
        return jsonify(analysis), 200
        
    except Exception as e:
        print(f"Error in get_disruption_analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ========================
# Main Entry Point
# ========================

if __name__ == "__main__":
    print("="*80)
    print("FLASK API SERVER - AIRLINE DISRUPTION MANAGEMENT SYSTEM")
    print("="*80)
    print("\nAPI Documentation:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/flights - List all flights")
    print("  GET  /api/flights/<id> - Flight details")
    print("  GET  /api/flights/<id>/passengers - Flight passengers with filters")
    print("  GET  /api/disruptions - All disruptions")
    print("  GET  /api/disruptions/<id>/recommendations - Get recommendations")
    print("  GET  /api/manager-summary - Manager dashboard summary")
    print("  POST /api/recommendations/generate - Trigger LLM")
    print("  POST /api/actions/apply-plan - Apply passenger plan")
    print("  POST /api/actions/approve-execute - Approve & execute")
    print("\nServer running on http://localhost:5000")
    print("="*80 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
