"""
Generate all_flights.json and guest_data.json with proper airline data schema
"""
import json
import random
import uuid
from datetime import datetime, timedelta

# Flight routes with realistic data
ROUTES = [
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "JFK", "duration": "PT13H36M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "LHR", "duration": "PT7H45M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "CDG", "duration": "PT7H30M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "SYD", "duration": "PT14H20M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "BOM", "duration": "PT3H30M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "ICN", "duration": "PT8H15M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "SIN", "duration": "PT7H00M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "BKK", "duration": "PT6H30M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "DXB", "duration": "PT1H15M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "DEL", "duration": "PT3H45M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "LAX", "duration": "PT16H20M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "ORD", "duration": "PT14H45M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "FRA", "duration": "PT7H15M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "MAD", "duration": "PT6H50M"},
    {"airline": "EY", "sched_dep": "AUH", "sched_arr": "MAN", "duration": "PT7H40M"},
]

AIRCRAFT_TYPES = [
    {"code": "351", "name": "A350-900", "seats": 371},
    {"code": "388", "name": "A380-800", "seats": 555},
    {"code": "777", "name": "B777-300ER", "seats": 396},
    {"code": "787", "name": "B787-10", "seats": 330},
]

CABINS = {
    "J": {"name": "Business", "seats": 44},
    "Y": {"name": "Economy", "seats": 327},
}

FIRST_NAMES = ["John", "Sarah", "Ahmed", "Maria", "Rajesh", "Lisa", "Chen", "Anna", "Hassan", "Emma",
               "Yuki", "Marco", "Amira", "James", "Sophie", "Dmitry", "Priya", "David", "Alexey", "Sophia"]

LAST_NAMES = ["Smith", "Johnson", "Ahmed", "Garcia", "Kumar", "Brown", "Wang", "Martinez", "Hassan", "Davis",
              "Tanaka", "Rossi", "Ibrahim", "Wilson", "Martin", "Fedotov", "Singh", "Taylor", "Sokolov", "Meyer"]

NATIONALITIES = ["USA", "GBR", "AUS", "CAN", "IND", "CHN", "JPN", "DEU", "FRA", "AE", "RUS", "BRA", "MEX", "KOR", "THA"]

def generate_flights(num_flights=15):
    """Generate flight data"""
    flights = []
    base_date = datetime(2025, 11, 26)
    
    for i in range(num_flights):
        route = ROUTES[i % len(ROUTES)]
        aircraft = random.choice(AIRCRAFT_TYPES)
        flight_num = str(i + 1).zfill(3)
        
        # Determine if this flight is disrupted
        is_disrupted = i < 4  # First 4 flights are disrupted
        
        # Create cabin classes
        cabin_classes = []
        j_pax = 40 if random.random() > 0.3 else 35
        y_capacity = aircraft["seats"] - CABINS["J"]["seats"]
        y_pax = random.randint(300, 320)
        
        cabin_classes.append({
            "Class": "J",
            "SeatCapacity": str(CABINS["J"]["seats"]),
            "Planned_PaxCount": str(j_pax),
            "Actual_PaxCount": str(j_pax)
        })
        cabin_classes.append({
            "Class": "Y",
            "SeatCapacity": str(y_capacity),
            "Planned_PaxCount": str(y_pax),
            "Actual_PaxCount": str(y_pax)
        })
        
        departure_dt = base_date + timedelta(days=random.randint(0, 3), hours=random.randint(0, 23))
        
        # Disruption info
        delay = 0
        dep_status = "OFB"
        arr_status = "ONB"
        flight_status = "ONB"
        delay_remarks = None
        
        if is_disrupted:
            disruption_types = ["Weather Conditions", "Crew Unavailable", "Aircraft Maintenance", "Catering Delay"]
            delay = random.choice([120, 150, 240, 300])  # minutes
            delay_remarks = random.choice(disruption_types)
            dep_status = "DEL"
            flight_status = "DEL"
        
        flight = {
            "flightkey": f"EY-{flight_num}-{departure_dt.strftime('%Y-%m-%d')}-{route['sched_dep']}-{route['sched_arr']}-1",
            "airline": "EY",
            "flightnumber": flight_num,
            "operationalsuffix": None,
            "sched_departureairport": route["sched_dep"],
            "sched_arrivalairport": route["sched_arr"],
            "actual_departureairport": route["sched_dep"],
            "actual_arrivalairport": route["sched_arr"],
            "departuredate": f"{departure_dt.strftime('%Y-%m-%d')}Z",
            "departurestatus": dep_status,
            "arrivalstatus": arr_status,
            "flight_type": "J",
            "flight_status": flight_status,
            "flight_status_transformed": flight_status,
            "PlannedArrivalAptHistory": route["sched_arr"],
            "legstatus": None,
            "tailnbr": f"A6{chr(65 + random.randint(0, 25))}{chr(65 + random.randint(0, 25))}{chr(65 + random.randint(0, 25))}",
            "cancellation_code": None,
            "repeatnumber": "1",
            "servicetype": "J",
            "CabinClass": cabin_classes,
            "callsign": f"ETD{flight_num}",
            "std_z_date": departure_dt.strftime('%Y-%m-%d'),
            "std_ls_date": (departure_dt + timedelta(hours=4)).strftime('%Y-%m-%d'),
            "std_z_date_time": departure_dt.strftime('%H:%M'),
            "std_ls_date_time": (departure_dt + timedelta(hours=4)).strftime('%H:%M'),
            "delay_remarks": delay_remarks,
            "estflightduration": route["duration"],
            "flightduration_hhmm": "".join(route["duration"].replace("PT", "").replace("H", "").replace("M", "").split(":")),
            "ownerairline_airline": "EY",
            "flightcrewairline": "EY",
            "cabincrewairline": "EY",
            "flightcycles": "1",
            "timeoffset_departure": "+240",
            "timeoffset_arrival": random.choice(["-300", "-500", "+100", "+430"]),
            "assaircft_upline_airline": "EY",
            "assaircft_upline_flightnumber": str(random.randint(100, 999)),
            "assaircft_upline_operationalsuffix": None,
            "assaircft_upline_departureairport": random.choice(["DEL", "BOM", "SYD", "NRT", "HND"]),
            "assaircft_upline_arrivalairport": "AUH",
            "assaircft_upline_origindate": f"{(departure_dt - timedelta(days=1)).strftime('%Y-%m-%d')}Z",
            "assaircft_upline_repeatnumber": "1",
            "assaircft_downline_airline": "EY",
            "assaircft_downline_flightnumber": str(random.randint(100, 999)),
            "assaircft_downline_operationalsuffix": None,
            "assaircft_downline_departureairport": route["sched_arr"],
            "assaircft_downline_arrivalairport": "AUH",
            "assaircft_downline_origindate": f"{(departure_dt + timedelta(days=1)).strftime('%Y-%m-%d')}Z",
            "assaircft_downline_repeatnumber": "1",
            "assfltleg_upline_legschedule": [],
            "assfltleg_downline_legschedule": [],
            "flightidentifierkey": str(random.randint(1000000, 9999999)),
            "aircrafttype": aircraft["code"],
            "aircraftsubtype": aircraft["code"] + "B"
        }
        flights.append(flight)
    
    return flights

def generate_passengers(flights):
    """Generate passenger data for each flight"""
    passengers = []
    
    for flight in flights:
        flight_num = flight["flightnumber"]
        total_pax = 0
        for cabin in flight["CabinClass"]:
            total_pax += int(cabin["Actual_PaxCount"])
        
        # Generate 300+ passengers per flight
        num_pax = random.randint(300, 340)
        
        for p in range(num_pax):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            
            # Determine cabin
            cabin = "J" if random.random() < 0.12 else "Y"
            seat_row = random.randint(1, 50 if cabin == "Y" else 15)
            seat_letter = random.choice(["A", "B", "C", "D", "E", "F"])
            seat = f"{seat_row:03d}{seat_letter}"
            
            pax_key = f"{uuid.uuid4().hex.upper()}_{uuid.uuid4().hex.upper()}"
            leg_delivery_id = f"{uuid.uuid4().hex.upper()}-{flight['sched_departureairport']}"
            
            # Determine if passenger is disrupted
            is_disrupted = flight["flight_status"] == "DEL"
            pax_status = "DISRUPTED" if is_disrupted else "NOT_DISRUPTED"
            
            # Create next segment for connections (30% of passengers)
            has_connection = random.random() < 0.3
            next_segment = None
            if has_connection:
                next_airport = random.choice([a for a in ["JFK", "LHR", "CDG", "SYD", "DEL"] if a != flight["sched_arrivalairport"]])
                next_segment = {
                    "next_segmentDeliveries_id": uuid.uuid4().hex.upper(),
                    "next_segment_departure_iataCode": flight["sched_arrivalairport"],
                    "next_segment_departure_time": f"{datetime.strptime(flight['std_z_date'], '%Y-%m-%d').strftime('%Y-%m-%d')}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00Z",
                    "next_segment_departure_time_utc": f"{datetime.strptime(flight['std_z_date'], '%Y-%m-%d').strftime('%Y-%m-%d')} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
                    "next_segment_arrival_iataCode": next_airport,
                    "next_segment_arrival_time": f"{(datetime.strptime(flight['std_z_date'], '%Y-%m-%d') + timedelta(hours=random.randint(6, 12))).strftime('%Y-%m-%dT%H:%M:%S')}Z",
                    "next_segment_arrival_time_utc": f"{(datetime.strptime(flight['std_z_date'], '%Y-%m-%d') + timedelta(hours=random.randint(6, 12))).strftime('%Y-%m-%d %H:%M:%S')}",
                    "next_segment_class": "E",
                    "next_segment_cabin": cabin,
                    "next_segment_statusCode": "HK",
                    "next_segment_marketingCarrierCode": "EY",
                    "next_segment_marketingFlightNumber": str(random.randint(100, 999)),
                    "next_segment_operatingCarrierCode": "EY",
                    "next_segment_operatingFlightNumber": str(random.randint(100, 999)),
                }
            
            passenger = {
                "dcsid": uuid.uuid4().hex.upper(),
                "paxkey": pax_key,
                "id": f"{pax_key}_REF",
                "lastModification_datetime": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z",
                "processed_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                "processed_date": datetime.now().strftime('%Y-%m-%d'),
                "time_generated": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                "segmentDeliveries_id": uuid.uuid4().hex.upper(),
                "legDeliveries_id": leg_delivery_id,
                "original_cabin_code": cabin,
                "segment_departure_iataCode": flight["sched_departureairport"],
                "segment_departure_time": f"{datetime.strptime(flight['std_z_date'], '%Y-%m-%d').strftime('%Y-%m-%d')}T{flight['std_z_date_time']}:00Z",
                "segment_departure_time_utc": f"{datetime.strptime(flight['std_z_date'], '%Y-%m-%d').strftime('%Y-%m-%d')} {flight['std_z_date_time']}:00",
                "segment_arrival_iataCode": flight["sched_arrivalairport"],
                "segment_arrival_time": f"{(datetime.strptime(flight['std_z_date'], '%Y-%m-%d') + timedelta(hours=int(flight['flightduration_hhmm'][:2]))).strftime('%Y-%m-%dT%H:%M:%S')}Z",
                "segment_arrival_time_utc": f"{(datetime.strptime(flight['std_z_date'], '%Y-%m-%d') + timedelta(hours=int(flight['flightduration_hhmm'][:2]))).strftime('%Y-%m-%d %H:%M:%S')}",
                "segment_class": "E",
                "segment_cabin": cabin,
                "segment_statusCode": "TK",
                "segment_marketingCarrierCode": "EY",
                "segment_marketingFlightNumber": flight_num,
                "segment_operatingCarrierCode": "EY",
                "segment_operatingFlightNumber": flight_num,
                "acceptedOnwardId": uuid.uuid4().hex.upper() if has_connection else None,
                "associatedPassengerSegments_informative_onward_id": uuid.uuid4().hex.upper() if has_connection else None,
                "associatedPassengerSegments_misconnected_onward_id": None,
                "associatedPassengerSegments_tci_onward_id": uuid.uuid4().hex.upper() if has_connection else None,
                "legDeliveries_departure_iataCode": flight["sched_departureairport"],
                "legDeliveries_departure_at": flight["std_z_date"],
                "legDeliveries_arrival_iataCode": flight["sched_arrivalairport"],
                "legDeliveries_arrival_at": None,
                "legDeliveries_operatingFlight_number": flight_num,
                "legDeliveries_operatingFlight_carrierCode": "EY",
                "legDeliveries_travelCabinCode": cabin,
                "legDeliveries_acceptance_securityNumber": f"{flight['sched_departureairport']}-{str(p).zfill(3)}",
                "legDeliveries_acceptance_status": "ACCEPTED",
                "legDeliveries_acceptance_acceptanceType": "PRIMARY",
                "legDeliveries_acceptance_isAdvanceAccepted": "false",
                "legDeliveries_acceptance_channel": random.choice(["WEB", "MOBILE", "KIOSK", "COUNTER"]),
                "seat_number": seat,
                "seat_characteristicsCodes": "N,CH,RS,9,ES",
                "seat_status": None,
                "boardingStatus": random.choice(["BOARDED_BY_SWIPE", "BOARDING", "NOT_BOARDED"]),
                "boardingZone": str(random.randint(1, 5)),
                "boardingPassPrint_status": random.choice(["PRINTED", "MOBILE", "NOT_PRINTED"]),
                "boardingPassPrint_channel": random.choice(["WEB", "MOBILE", "COUNTER"]),
                "boarding_deviceId": None,
                "boarding_referenceDeviceType": None,
                "boarding_utcDateTime": None,
                "flightTransfer_id": None,
                "subType": None,
                "dcsTransferStatus": None,
                "disruptionTransferReason": None,
                "current_flight_rebooked_from": [],
                "connecting_flight_rebooked_from": [],
                "next_segmentDeliveries_id": next_segment["next_segmentDeliveries_id"] if next_segment else None,
                "next_segment_departure_iataCode": next_segment["next_segment_departure_iataCode"] if next_segment else None,
                "next_segment_departure_time": next_segment["next_segment_departure_time"] if next_segment else None,
                "next_segment_departure_time_utc": next_segment["next_segment_departure_time_utc"] if next_segment else None,
                "next_segment_arrival_iataCode": next_segment["next_segment_arrival_iataCode"] if next_segment else None,
                "next_segment_arrival_time": next_segment["next_segment_arrival_time"] if next_segment else None,
                "next_segment_arrival_time_utc": next_segment["next_segment_arrival_time_utc"] if next_segment else None,
                "next_segment_class": next_segment["next_segment_class"] if next_segment else None,
                "next_segment_cabin": next_segment["next_segment_cabin"] if next_segment else None,
                "next_segment_statusCode": next_segment["next_segment_statusCode"] if next_segment else None,
                "next_segment_marketingCarrierCode": next_segment["next_segment_marketingCarrierCode"] if next_segment else None,
                "next_segment_marketingFlightNumber": next_segment["next_segment_marketingFlightNumber"] if next_segment else None,
                "next_segment_operatingCarrierCode": next_segment["next_segment_operatingCarrierCode"] if next_segment else None,
                "next_segment_operatingFlightNumber": next_segment["next_segment_operatingFlightNumber"] if next_segment else None,
                "next_associatedPassengerSegments_informative_onward_id": None,
                "next_associatedPassengerSegments_misconnected_onward_id": None,
                "next_associatedPassengerSegments_tci_onward_id": None,
                "next_legDeliveries_id": f"{next_segment['next_segmentDeliveries_id']}-{flight['sched_arrivalairport']}" if next_segment else None,
                "next_legDeliveries_departure_iataCode": next_segment["next_segment_departure_iataCode"] if next_segment else None,
                "next_legDeliveries_departure_at": next_segment["next_segment_departure_time"].split("T")[0] if next_segment else None,
                "next_legDeliveries_arrival_iataCode": next_segment["next_segment_arrival_iataCode"] if next_segment else None,
                "next_legDeliveries_arrival_at": None,
                "next_legDeliveries_operatingFlight_number": next_segment["next_segment_operatingFlightNumber"] if next_segment else None,
                "next_legDeliveries_operatingFlight_carrierCode": next_segment["next_segment_operatingCarrierCode"] if next_segment else None,
                "next_legDeliveries_travelCabinCode": next_segment["next_segment_cabin"] if next_segment else None,
                "previous_segmentDeliveries_id": None,
                "previous_segment_departure_iataCode": None,
                "previous_segment_departure_time": None,
                "previous_segment_departure_time_utc": None,
                "previous_segment_arrival_iataCode": None,
                "previous_segment_arrival_time": None,
                "previous_segment_arrival_time_utc": None,
                "previous_segment_class": None,
                "previous_segment_cabin": None,
                "previous_segment_statusCode": None,
                "previous_segment_marketingCarrierCode": None,
                "previous_segment_marketingFlightNumber": None,
                "previous_segment_operatingCarrierCode": None,
                "previous_segment_operatingFlightNumber": None,
                "previous_associatedPassengerSegments_informative_onward_id": None,
                "previous_associatedPassengerSegments_misconnected_onward_id": None,
                "previous_associatedPassengerSegments_tci_onward_id": None,
                "previous_legDeliveries_id": None,
                "previous_legDeliveries_departure_iataCode": None,
                "previous_legDeliveries_departure_at": None,
                "previous_legDeliveries_arrival_iataCode": None,
                "previous_legDeliveries_arrival_at": None,
                "previous_legDeliveries_operatingFlight_number": None,
                "previous_legDeliveries_operatingFlight_carrierCode": None,
                "previous_legDeliveries_travelCabinCode": None,
                "contactsText": None,
                "contactsEmail": f"{first_name.lower()}.{last_name.lower()}@email.com",
                "contactsCountryCode": None,
                "contactPurpose": random.choice(["EMERGENCY", "GENERAL", "MARKETING"]),
                "passengerDisruptionStatus": pax_status,
                "Nationality": random.choice(NATIONALITIES),
                "regulatoryDocuments": [
                    {
                        "id": uuid.uuid4().hex.upper(),
                        "document": json.dumps({
                            "documentType": "PASSPORT",
                            "number": str(random.randint(1000000, 9999999)),
                            "expiryDate": (datetime.now() + timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                            "issuanceCountry": random.choice(NATIONALITIES),
                            "name": {"firstName": first_name, "lastName": last_name}
                        }),
                        "validForCarrier": "EY",
                        "isCarried": "true"
                    }
                ],
                "dcsProductType": "ACTIVE_SYNCHRONISED",
                "passengerLinks": [
                    {
                        "id": uuid.uuid4().hex.upper(),
                        "collection": json.dumps([
                            {"id": uuid.uuid4().hex.upper(), "type": "CUSTOMER_LINK"},
                            {"id": uuid.uuid4().hex.upper(), "type": "CUSTOMER_LINK"}
                        ])
                    }
                ],
                "PNR": ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6)),
                "passenger_firstName": first_name,
                "passenger_lastName": last_name,
                "passenger_title": random.choice(["MR", "MS", "MRS", None]),
                "passenger_dateOfBirth": f"{random.randint(1950, 2010)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "passenger_gender": random.choice(["MALE", "FEMALE"]),
                "passenger_flightPassengerType": random.choice(["ADULT", "CHILD", "INFANT"]),
                "frequentFlyer": random.choice([f"EY{random.randint(100000, 999999)}", None])
            }
            passengers.append(passenger)
    
    return passengers

if __name__ == "__main__":
    print("Generating flight data...")
    flights = generate_flights(15)
    
    print("Generating passenger data...")
    passengers = generate_passengers(flights)
    
    # Save files
    with open("all_flights.json", "w") as f:
        json.dump(flights, f, indent=2)
    print(f"✅ Saved all_flights.json with {len(flights)} flights")
    
    with open("guest_data.json", "w") as f:
        json.dump(passengers, f, indent=2)
    print(f"✅ Saved guest_data.json with {len(passengers)} passengers")
    
    print(f"\nSummary:")
    print(f"  - Flights: {len(flights)}")
    print(f"  - Total passengers: {len(passengers)}")
    print(f"  - Avg passengers per flight: {len(passengers) // len(flights)}")
    print(f"  - Disrupted flights: {sum(1 for f in flights if f['flight_status'] == 'DEL')}")
