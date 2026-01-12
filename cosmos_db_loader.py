"""
Azure Cosmos DB Data Loader for Airline Disruption Management System
Loads flight and passenger data into Cosmos DB Emulator
"""

import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os

# Cosmos DB Emulator Configuration
COSMOS_ENDPOINT = "https://localhost:8081"
COSMOS_KEY = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
DATABASE_NAME = "HACK-AI-THON"
FLIGHTS_CONTAINER = "flights_data"
PASSENGERS_CONTAINER = "passengers_data"
DISRUPTIONS_CONTAINER = "disruptions"

def create_cosmos_client():
    """Create and return Cosmos DB client"""
    try:
        # Disable SSL warnings for emulator
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Create client with SSL verification disabled for emulator
        import warnings
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        
        client = CosmosClient(
            COSMOS_ENDPOINT, 
            COSMOS_KEY, 
            connection_verify=False
        )
        print("✓ Connected to Cosmos DB Emulator")
        return client
    except Exception as e:
        print(f"✗ Failed to connect to Cosmos DB Emulator: {e}")
        print("\nMake sure:")
        print("1. Cosmos DB Emulator is running")
        print("2. You have accepted the SSL certificate")
        raise

def create_database_and_containers(client):
    """Create database and containers with appropriate partition keys"""
    try:
        # Get existing database
        try:
            database = client.get_database_client(DATABASE_NAME)
            print(f"✓ Connected to existing database: {DATABASE_NAME}")
        except:
            database = client.create_database(DATABASE_NAME)
            print(f"✓ Created database: {DATABASE_NAME}")
        
        # Create Flights container
        # Partition key: flight_date (for efficient date-based queries)
        try:
            flights_container = database.create_container(
                id=FLIGHTS_CONTAINER,
                partition_key=PartitionKey(path="/flight_date"),
                offer_throughput=400
            )
            print(f"✓ Created container: {FLIGHTS_CONTAINER}")
        except exceptions.CosmosResourceExistsError:
            flights_container = database.get_container_client(FLIGHTS_CONTAINER)
            print(f"✓ Container already exists: {FLIGHTS_CONTAINER}")
        
        # Create Passengers container
        # Partition key: flight_id (to keep all passengers of a flight together)
        try:
            passengers_container = database.create_container(
                id=PASSENGERS_CONTAINER,
                partition_key=PartitionKey(path="/flight_id"),
                offer_throughput=400
            )
            print(f"✓ Created container: {PASSENGERS_CONTAINER}")
        except exceptions.CosmosResourceExistsError:
            passengers_container = database.get_container_client(PASSENGERS_CONTAINER)
            print(f"✓ Container already exists: {PASSENGERS_CONTAINER}")
        
        # Create Disruptions container for event tracking
        # Partition key: disruption_date
        try:
            disruptions_container = database.create_container(
                id=DISRUPTIONS_CONTAINER,
                partition_key=PartitionKey(path="/disruption_date"),
                offer_throughput=400
            )
            print(f"✓ Created container: {DISRUPTIONS_CONTAINER}")
        except exceptions.CosmosResourceExistsError:
            disruptions_container = database.get_container_client(DISRUPTIONS_CONTAINER)
            print(f"✓ Container already exists: {DISRUPTIONS_CONTAINER}")
        
        return database, flights_container, passengers_container, disruptions_container
        
    except Exception as e:
        print(f"✗ Error creating database/containers: {e}")
        raise

def load_flights_data(container, file_path="test_data/flights_data.json"):
    """Load flights data into Cosmos DB"""
    try:
        with open(file_path, 'r') as f:
            flights = json.load(f)
        
        print(f"\nLoading {len(flights)} flights...")
        success_count = 0
        error_count = 0
        
        for flight in flights:
            try:
                # Add id field for Cosmos DB (using flight_id)
                flight['id'] = flight['flight_id']
                container.create_item(body=flight)
                success_count += 1
                print(f"  ✓ Loaded flight {flight['flight_number']} ({success_count}/{len(flights)})")
            except exceptions.CosmosResourceExistsError:
                # Update existing item
                container.upsert_item(body=flight)
                success_count += 1
                print(f"  ↻ Updated flight {flight['flight_number']} ({success_count}/{len(flights)})")
            except Exception as e:
                error_count += 1
                print(f"  ✗ Error loading flight {flight.get('flight_number', 'unknown')}: {e}")
        
        print(f"\n✓ Flights loaded: {success_count} successful, {error_count} errors")
        return success_count, error_count
        
    except Exception as e:
        print(f"✗ Error loading flights data: {e}")
        raise

def load_passengers_data(container, file_path="test_data/passengers_data.json"):
    """Load passengers data into Cosmos DB"""
    try:
        with open(file_path, 'r') as f:
            passengers = json.load(f)
        
        print(f"\nLoading {len(passengers)} passengers...")
        success_count = 0
        error_count = 0
        
        for i, passenger in enumerate(passengers):
            try:
                # Add id field for Cosmos DB (using passenger_id)
                passenger['id'] = passenger['passenger_id']
                container.create_item(body=passenger)
                success_count += 1
                
                # Print progress every 500 passengers
                if (i + 1) % 500 == 0:
                    print(f"  ✓ Loaded {success_count}/{len(passengers)} passengers...")
                    
            except exceptions.CosmosResourceExistsError:
                # Update existing item
                container.upsert_item(body=passenger)
                success_count += 1
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Only print first 5 errors
                    print(f"  ✗ Error loading passenger {passenger.get('pnr', 'unknown')}: {e}")
        
        print(f"\n✓ Passengers loaded: {success_count} successful, {error_count} errors")
        return success_count, error_count
        
    except Exception as e:
        print(f"✗ Error loading passengers data: {e}")
        raise

def create_disruption_events(disruptions_container, flights_container, database):
    """Create disruption event records for non-on-time flights"""
    try:
        # Query for disrupted flights
        query = "SELECT * FROM c WHERE c.disruption_status != 'On Time'"
        
        flights_container_client = database.get_container_client(FLIGHTS_CONTAINER)
        disrupted_flights = list(flights_container_client.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        print(f"\nCreating disruption events for {len(disrupted_flights)} disrupted flights...")
        success_count = 0
        
        for flight in disrupted_flights:
            try:
                disruption_event = {
                    "id": f"disruption_{flight['flight_id']}",
                    "disruption_id": f"disruption_{flight['flight_id']}",
                    "flight_id": flight['flight_id'],
                    "flight_number": flight['flight_number'],
                    "flight_date": flight['flight_date'],
                    "disruption_date": flight['flight_date'],
                    "disruption_status": flight['disruption_status'],
                    "disruption_reason": flight['disruption_reason'],
                    "delay_minutes": flight.get('delay_minutes', 0),
                    "origin": flight['origin'],
                    "destination": flight['destination'],
                    "scheduled_departure": flight['scheduled_departure'],
                    "estimated_departure": flight['estimated_departure'],
                    "detected_at": flight['scheduled_departure'],
                    "status": "Pending Review",
                    "passengers_affected": 0,  # Will be updated
                    "actions_taken": []
                }
                
                disruptions_container.upsert_item(body=disruption_event)
                success_count += 1
                print(f"  ✓ Created disruption event for {flight['flight_number']}")
                
            except Exception as e:
                print(f"  ✗ Error creating disruption event for {flight['flight_number']}: {e}")
        
        print(f"\n✓ Created {success_count} disruption events")
        return success_count
        
    except Exception as e:
        print(f"✗ Error creating disruption events: {e}")
        raise

def verify_data_load(database):
    """Verify data has been loaded correctly"""
    try:
        print("\n" + "="*80)
        print("DATA VERIFICATION")
        print("="*80)
        
        # Count flights
        flights_container = database.get_container_client(FLIGHTS_CONTAINER)
        flights_query = "SELECT VALUE COUNT(1) FROM c"
        flight_count = list(flights_container.query_items(
            query=flights_query,
            enable_cross_partition_query=True
        ))[0]
        print(f"\n✓ Total Flights in DB: {flight_count}")
        
        # Count passengers
        passengers_container = database.get_container_client(PASSENGERS_CONTAINER)
        passengers_query = "SELECT VALUE COUNT(1) FROM c"
        passenger_count = list(passengers_container.query_items(
            query=passengers_query,
            enable_cross_partition_query=True
        ))[0]
        print(f"✓ Total Passengers in DB: {passenger_count}")
        
        # Count disruptions
        disruptions_container = database.get_container_client(DISRUPTIONS_CONTAINER)
        disruptions_query = "SELECT VALUE COUNT(1) FROM c"
        disruption_count = list(disruptions_container.query_items(
            query=disruptions_query,
            enable_cross_partition_query=True
        ))[0]
        print(f"✓ Total Disruption Events in DB: {disruption_count}")
        
        # Query disrupted flights
        disrupted_flights_query = "SELECT c.flight_number, c.disruption_status, c.disruption_reason FROM c WHERE c.disruption_status != 'On Time'"
        disrupted_flights = list(flights_container.query_items(
            query=disrupted_flights_query,
            enable_cross_partition_query=True
        ))
        
        print(f"\n✓ Disrupted Flights:")
        for flight in disrupted_flights:
            print(f"  - {flight['flight_number']}: {flight['disruption_status']} - {flight.get('disruption_reason', 'N/A')}")
        
        print("\n" + "="*80)
        print("✓ Data verification complete!")
        print("="*80)
        
    except Exception as e:
        print(f"✗ Error during verification: {e}")
        raise

def main():
    """Main execution function"""
    print("="*80)
    print("AZURE COSMOS DB DATA LOADER")
    print("Airline Disruption Management System")
    print("="*80)
    
    try:
        # Step 1: Create client
        client = create_cosmos_client()
        
        # Step 2: Create database and containers
        database, flights_container, passengers_container, disruptions_container = create_database_and_containers(client)
        
        # Step 3: Load flights data
        flights_success, flights_errors = load_flights_data(flights_container)
        
        # Step 4: Load passengers data
        passengers_success, passengers_errors = load_passengers_data(passengers_container)
        
        # Step 5: Create disruption events
        disruption_count = create_disruption_events(disruptions_container, flights_container, database)
        
        # Step 6: Verify data
        verify_data_load(database)
        
        print("\n" + "="*80)
        print("✓ DATA LOADING COMPLETE!")
        print("="*80)
        print(f"Database: {DATABASE_NAME}")
        print(f"Flights loaded: {flights_success}")
        print(f"Passengers loaded: {passengers_success}")
        print(f"Disruption events created: {disruption_count}")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        print("\nPlease ensure:")
        print("1. Cosmos DB Emulator is running")
        print("2. SSL certificate is accepted")
        print("3. Test data files exist in test_data/ folder")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
