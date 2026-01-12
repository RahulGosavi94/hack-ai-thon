"""
Data Loader for Cosmos DB Emulator (using older SDK v3)
"""

import json
import azure.cosmos.cosmos_client as cosmos_client

# Configuration
HOST = 'https://localhost:1234'
MASTER_KEY = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
DATABASE_ID = 'HACK-AI-THON'
FLIGHTS_CONTAINER_ID = 'flights_data'
PASSENGERS_CONTAINER_ID = 'passengers_data'

def main():
    print("="*80)
    print("LOADING DATA INTO COSMOS DB EMULATOR")
    print("="*80)
    
    try:
        # Connect to Cosmos DB
        print("\n1. Connecting to Cosmos DB Emulator...")
        client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})
        print("   ✓ Connected successfully")
        
        # Get database
        print(f"\n2. Accessing database: {DATABASE_ID}...")
        database = client.get_database_client(DATABASE_ID)
        print("   ✓ Database accessed")
        
        # Get containers
        print(f"\n3. Accessing containers...")
        flights_container = database.get_container_client(FLIGHTS_CONTAINER_ID)
        passengers_container = database.get_container_client(PASSENGERS_CONTAINER_ID)
        print(f"   ✓ Container '{FLIGHTS_CONTAINER_ID}' ready")
        print(f"   ✓ Container '{PASSENGERS_CONTAINER_ID}' ready")
        
        # Load flights
        print(f"\n4. Loading flights data...")
        with open("test_data/flights_data.json", 'r') as f:
            flights = json.load(f)
        
        flight_count = 0
        for flight in flights:
            try:
                flight['id'] = flight['flight_id']
                flights_container.upsert_item(body=flight)
                flight_count += 1
                print(f"   ✓ Loaded flight {flight['flight_number']} ({flight_count}/{len(flights)})")
            except Exception as e:
                print(f"   ✗ Error with flight {flight['flight_number']}: {e}")
        
        print(f"\n   ✓ Successfully loaded {flight_count} flights")
        
        # Load passengers
        print(f"\n5. Loading passengers data...")
        with open("test_data/passengers_data.json", 'r') as f:
            passengers = json.load(f)
        
        passenger_count = 0
        for i, passenger in enumerate(passengers):
            try:
                passenger['id'] = passenger['passenger_id']
                passengers_container.upsert_item(body=passenger)
                passenger_count += 1
                
                # Show progress every 500 passengers
                if (i + 1) % 500 == 0:
                    print(f"   ✓ Progress: {passenger_count}/{len(passengers)} passengers loaded...")
            except Exception as e:
                if passenger_count < 5:
                    print(f"   ✗ Error with passenger {passenger.get('pnr', 'unknown')}: {e}")
        
        print(f"\n   ✓ Successfully loaded {passenger_count} passengers")
        
        # Verify data
        print(f"\n6. Verifying data...")
        
        # Query disrupted flights
        disrupted_query = "SELECT c.flight_number, c.disruption_status, c.disruption_reason FROM c WHERE c.disruption_status != 'On Time'"
        disrupted_flights = list(flights_container.query_items(
            query=disrupted_query,
            enable_cross_partition_query=True
        ))
        
        print(f"   ✓ Total flights loaded: {flight_count}")
        print(f"   ✓ Total passengers loaded: {passenger_count}")
        print(f"   ✓ Disrupted flights: {len(disrupted_flights)}")
        
        for flight in disrupted_flights:
            print(f"      - {flight['flight_number']}: {flight['disruption_status']} ({flight.get('disruption_reason', 'N/A')})")
        
        print("\n" + "="*80)
        print("✓ DATA LOADING COMPLETE!")
        print("="*80)
        print(f"Database: {DATABASE_ID}")
        print(f"Flights loaded: {flight_count}")
        print(f"Passengers loaded: {passenger_count}")
        print(f"Disrupted flights: {len(disrupted_flights)}")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
