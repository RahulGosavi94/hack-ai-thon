"""
Disruption Detection Engine
Monitors flight data and detects operational issues that require intervention
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class DisruptionSeverity(Enum):
    """Severity levels for disruptions"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class DisruptionType(Enum):
    """Types of disruptions"""
    DELAY = "Delay"
    CANCELLATION = "Cancellation"
    AIRCRAFT_SWAP = "Aircraft Swap"
    DIVERSION = "Diversion"
    CREW_ISSUE = "Crew Issue"
    TECHNICAL = "Technical Issue"
    WEATHER = "Weather"

@dataclass
class DisruptionEvent:
    """Represents a detected disruption event"""
    disruption_id: str
    flight_id: str
    flight_number: str
    flight_date: str
    origin: str
    destination: str
    disruption_type: str
    disruption_status: str
    disruption_reason: str
    severity: str
    delay_minutes: int
    scheduled_departure: str
    estimated_departure: str
    passengers_affected: int
    high_value_passengers: int
    connecting_passengers: int
    detected_at: str
    requires_rebooking: bool
    requires_accommodation: bool
    estimated_cost_impact: float
    affected_passenger_list: List[Dict]  # Full passenger details
    high_value_passenger_list: List[Dict]  # High-value passengers needing priority
    connecting_passenger_list: List[Dict]  # Passengers with connections at risk
    
    def to_dict(self):
        return asdict(self)

class DisruptionDetector:
    """Main disruption detection engine"""
    
    # Detection thresholds
    DELAY_THRESHOLDS = {
        "minor": 30,      # < 30 min: Minor
        "moderate": 120,  # 30-120 min: Moderate
        "major": 240,     # 120-240 min: Major
        "severe": 240     # > 240 min: Severe
    }
    
    def __init__(self, flights_data_path: str, passengers_data_path: str):
        """Initialize detector with data sources"""
        self.flights = self._load_json(flights_data_path)
        self.passengers = self._load_json(passengers_data_path)
        self.disruptions: List[DisruptionEvent] = []
        
    def _load_json(self, file_path: str) -> List[Dict]:
        """Load JSON data from file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def detect_all_disruptions(self) -> List[DisruptionEvent]:
        """Scan all flights and detect disruptions"""
        print("="*80)
        print("DISRUPTION DETECTION ENGINE - SCANNING FLIGHTS")
        print("="*80)
        
        disrupted_flights = [f for f in self.flights if f['disruption_status'] != 'On Time']
        
        print(f"\n📊 Total flights: {len(self.flights)}")
        print(f"⚠️  Disrupted flights detected: {len(disrupted_flights)}")
        print("\n" + "-"*80)
        
        for flight in disrupted_flights:
            disruption = self._analyze_flight_disruption(flight)
            self.disruptions.append(disruption)
            self._print_disruption_summary(disruption)
        
        return self.disruptions
    
    def _analyze_flight_disruption(self, flight: Dict) -> DisruptionEvent:
        """Analyze a single disrupted flight"""
        # Get affected passengers (only those who have checked in or have boarding pass)
        all_passengers = [p for p in self.passengers if p['flight_id'] == flight['flight_id']]
        
        # Filter to only passengers who are likely to be affected
        # (checked in, at airport, or have boarding pass - not just booked)
        affected_passengers = [
            p for p in all_passengers 
            if p.get('check_in_status') == 'Checked In' or p.get('boarding_pass_issued', False)
        ]
        
        # If no one checked in yet but flight is soon, include everyone
        if not affected_passengers:
            affected_passengers = all_passengers
        
        # Identify high-value passengers (loyalty tier Gold/Platinum or Business/First class)
        high_value_passengers = [
            p for p in affected_passengers 
            if p.get('loyalty_tier') in ['Gold', 'Platinum'] or p.get('fare_class') in ['J', 'C']
        ]
        
        # Identify connecting passengers (simulate - in real world, check PNR for onwards flights)
        # For now, estimate based on long-haul routes and mark them
        is_long_haul = self._estimate_distance(flight['origin'], flight['destination']) > 3000
        connecting_ratio = 0.30 if is_long_haul else 0.15
        
        # Simulate which passengers have connections
        import random
        random.seed(flight['flight_id'])  # Consistent results
        connecting_passengers = [
            {**p, 'has_connection': True, 'connection_risk': 'High' if flight.get('delay_minutes', 0) > 90 else 'Medium'}
            for p in affected_passengers 
            if random.random() < connecting_ratio
        ]
        
        # Determine severity
        severity = self._calculate_severity(
            flight['disruption_status'],
            flight.get('delay_minutes', 0),
            len(affected_passengers),
            len(high_value_passengers)
        )
        
        # Check if rebooking needed
        requires_rebooking = flight['disruption_status'] == 'Cancelled'
        
        # Check if accommodation needed (delays > 4 hours or cancellations)
        requires_accommodation = (
            flight['disruption_status'] == 'Cancelled' or 
            flight.get('delay_minutes', 0) > 240
        )
        
        # Estimate cost impact
        cost_impact = self._estimate_cost_impact(
            flight,
            len(affected_passengers),
            requires_rebooking,
            requires_accommodation
        )
        
        # Prepare passenger lists for export
        affected_passenger_list = [
            {
                'passenger_id': p['passenger_id'],
                'pnr': p['pnr'],
                'full_name': p['full_name'],
                'email': p['email'],
                'phone': p['phone'],
                'fare_class': p['fare_class'],
                'fare_class_name': p['fare_class_name'],
                'seat_number': p['seat_number'],
                'loyalty_tier': p.get('loyalty_tier'),
                'frequent_flyer_number': p.get('frequent_flyer_number'),
                'check_in_status': p.get('check_in_status'),
                'boarding_pass_issued': p.get('boarding_pass_issued', False),
                'special_service_request': p.get('special_service_request'),
                'checked_bags': p.get('checked_bags', 0),
                'ticket_price_usd': p.get('ticket_price_usd', 0)
            }
            for p in affected_passengers
        ]
        
        high_value_passenger_list = [
            {
                'passenger_id': p['passenger_id'],
                'pnr': p['pnr'],
                'full_name': p['full_name'],
                'email': p['email'],
                'phone': p['phone'],
                'fare_class': p['fare_class'],
                'loyalty_tier': p.get('loyalty_tier'),
                'frequent_flyer_number': p.get('frequent_flyer_number'),
                'priority_level': 'High' if p.get('loyalty_tier') == 'Platinum' else 'Medium'
            }
            for p in high_value_passengers
        ]
        
        connecting_passenger_list = [
            {
                'passenger_id': p['passenger_id'],
                'pnr': p['pnr'],
                'full_name': p['full_name'],
                'email': p['email'],
                'phone': p['phone'],
                'fare_class': p['fare_class'],
                'loyalty_tier': p.get('loyalty_tier'),
                'has_connection': p['has_connection'],
                'connection_risk': p['connection_risk'],
                'needs_rebooking': p['connection_risk'] == 'High'
            }
            for p in connecting_passengers
        ]
        
        return DisruptionEvent(
            disruption_id=f"DISR_{flight['flight_id'][:8]}",
            flight_id=flight['flight_id'],
            flight_number=flight['flight_number'],
            flight_date=flight['flight_date'],
            origin=flight['origin'],
            destination=flight['destination'],
            disruption_type=self._map_disruption_type(flight['disruption_status']),
            disruption_status=flight['disruption_status'],
            disruption_reason=flight['disruption_reason'] or "Unknown",
            severity=severity.value,
            delay_minutes=flight.get('delay_minutes', 0),
            scheduled_departure=flight['scheduled_departure'],
            estimated_departure=flight['estimated_departure'],
            passengers_affected=len(affected_passengers),
            high_value_passengers=len(high_value_passengers),
            connecting_passengers=len(connecting_passengers),
            detected_at=datetime.now().isoformat(),
            requires_rebooking=requires_rebooking,
            requires_accommodation=requires_accommodation,
            estimated_cost_impact=cost_impact,
            affected_passenger_list=affected_passenger_list,
            high_value_passenger_list=high_value_passenger_list,
            connecting_passenger_list=connecting_passenger_list
        )
    
    def _calculate_severity(
        self, 
        status: str, 
        delay_minutes: int, 
        pax_count: int,
        high_value_pax: int
    ) -> DisruptionSeverity:
        """Calculate disruption severity based on multiple factors"""
        
        # Cancellations are always high severity
        if status == 'Cancelled':
            return DisruptionSeverity.CRITICAL
        
        # High value passenger impact
        if high_value_pax > 20:
            return DisruptionSeverity.HIGH
        
        # Delay-based severity
        if status == 'Delayed':
            if delay_minutes > 240:
                return DisruptionSeverity.CRITICAL
            elif delay_minutes > 120:
                return DisruptionSeverity.HIGH
            elif delay_minutes > 30:
                return DisruptionSeverity.MEDIUM
            else:
                return DisruptionSeverity.LOW
        
        # Aircraft swap or diversion
        if status in ['Aircraft Swap', 'Diverted']:
            return DisruptionSeverity.MEDIUM
        
        return DisruptionSeverity.LOW
    
    def _map_disruption_type(self, status: str) -> str:
        """Map disruption status to type"""
        mapping = {
            'Delayed': DisruptionType.DELAY.value,
            'Cancelled': DisruptionType.CANCELLATION.value,
            'Aircraft Swap': DisruptionType.AIRCRAFT_SWAP.value,
            'Diverted': DisruptionType.DIVERSION.value
        }
        return mapping.get(status, DisruptionType.DELAY.value)
    
    def _estimate_cost_impact(
        self, 
        flight: Dict, 
        pax_count: int,
        requires_rebooking: bool,
        requires_accommodation: bool
    ) -> float:
        """Estimate financial impact of disruption"""
        cost = 0.0
        
        # Compensation costs (EU261 style estimates)
        if requires_rebooking:  # Cancellation
            distance = self._estimate_distance(flight['origin'], flight['destination'])
            if distance < 1500:
                cost += pax_count * 250  # €250 per passenger
            elif distance < 3500:
                cost += pax_count * 400  # €400 per passenger
            else:
                cost += pax_count * 600  # €600 per passenger
        elif flight.get('delay_minutes', 0) > 180:
            # Delay compensation (reduced rates)
            cost += pax_count * 200
        
        # Accommodation costs
        if requires_accommodation:
            # Assume 60% need hotels at $150/night
            cost += (pax_count * 0.6) * 150
            # Meal vouchers for all
            cost += pax_count * 50
        
        # Rebooking operational costs
        if requires_rebooking:
            cost += pax_count * 100  # Staff time, system costs
        
        return round(cost, 2)
    
    def _estimate_distance(self, origin: str, destination: str) -> int:
        """Rough distance estimation for route (in km)"""
        # Simple lookup for common routes
        distances = {
            ('AUH', 'BOM'): 1900, ('AUH', 'DXB'): 130, ('AUH', 'DOH'): 350,
            ('AUH', 'LHR'): 5500, ('AUH', 'JFK'): 11000, ('AUH', 'SYD'): 12000,
            ('AUH', 'CDG'): 5200, ('AUH', 'FRA'): 4900, ('AUH', 'SIN'): 6300,
            ('AUH', 'BKK'): 4800, ('AUH', 'MEL'): 11000, ('AUH', 'MAD'): 5600,
            ('AUH', 'MAN'): 5400, ('AUH', 'LAX'): 13000, ('AUH', 'ICN'): 6500
        }
        return distances.get((origin, destination), 5000)
    
    def _print_disruption_summary(self, disruption: DisruptionEvent):
        """Print a summary of the detected disruption"""
        severity_emoji = {
            "Low": "🟢",
            "Medium": "🟡",
            "High": "🟠",
            "Critical": "🔴"
        }
        
        emoji = severity_emoji.get(disruption.severity, "⚪")
        
        print(f"\n{emoji} DISRUPTION DETECTED")
        print(f"   Flight: {disruption.flight_number} ({disruption.origin} → {disruption.destination})")
        print(f"   Type: {disruption.disruption_status}")
        print(f"   Reason: {disruption.disruption_reason}")
        print(f"   Severity: {disruption.severity}")
        if disruption.delay_minutes > 0:
            print(f"   Delay: {disruption.delay_minutes} minutes")
        print(f"   Passengers Affected: {disruption.passengers_affected}")
        print(f"   High-Value Passengers: {disruption.high_value_passengers}")
        print(f"   Connecting Passengers: {disruption.connecting_passengers}")
        print(f"   Requires Rebooking: {'Yes' if disruption.requires_rebooking else 'No'}")
        print(f"   Requires Accommodation: {'Yes' if disruption.requires_accommodation else 'No'}")
        print(f"   Est. Cost Impact: ${disruption.estimated_cost_impact:,.2f}")
        print(f"   Detected: {disruption.detected_at}")
        
        # Show sample of affected passengers
        if disruption.affected_passenger_list:
            print(f"\n   📋 Sample Affected Passengers (showing first 3):")
            for pax in disruption.affected_passenger_list[:3]:
                status = "✓ Checked In" if pax['check_in_status'] == 'Checked In' else "○ Not Checked In"
                print(f"      - {pax['full_name']} (PNR: {pax['pnr']}) - {pax['fare_class_name']} - {status}")
        
        # Show connecting passengers at risk
        if disruption.connecting_passenger_list:
            high_risk = [p for p in disruption.connecting_passenger_list if p['connection_risk'] == 'High']
            if high_risk:
                print(f"\n   🔄 Passengers at Risk of Missing Connections: {len(high_risk)}")
                for pax in high_risk[:2]:
                    print(f"      - {pax['full_name']} (PNR: {pax['pnr']}) - Connection at risk")
    
    def export_disruptions(self, output_path: str = "detected_disruptions.json"):
        """Export detected disruptions to JSON file"""
        data = {
            "detection_timestamp": datetime.now().isoformat(),
            "total_flights_scanned": len(self.flights),
            "total_disruptions_detected": len(self.disruptions),
            "total_passengers_affected": sum(d.passengers_affected for d in self.disruptions),
            "total_estimated_cost": sum(d.estimated_cost_impact for d in self.disruptions),
            "disruptions": [d.to_dict() for d in self.disruptions]
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return output_path
    
    def generate_summary_report(self) -> Dict:
        """Generate summary statistics"""
        if not self.disruptions:
            return {}
        
        severity_counts = {}
        for d in self.disruptions:
            severity_counts[d.severity] = severity_counts.get(d.severity, 0) + 1
        
        return {
            "total_disruptions": len(self.disruptions),
            "total_passengers_affected": sum(d.passengers_affected for d in self.disruptions),
            "total_high_value_passengers": sum(d.high_value_passengers for d in self.disruptions),
            "total_connecting_passengers": sum(d.connecting_passengers for d in self.disruptions),
            "severity_breakdown": severity_counts,
            "flights_requiring_rebooking": sum(1 for d in self.disruptions if d.requires_rebooking),
            "flights_requiring_accommodation": sum(1 for d in self.disruptions if d.requires_accommodation),
            "total_estimated_cost": sum(d.estimated_cost_impact for d in self.disruptions)
        }

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("AIRLINE DISRUPTION DETECTION ENGINE - INITIALIZING")
    print("="*80 + "\n")
    
    # Initialize detector
    detector = DisruptionDetector(
        flights_data_path="test_data/flights_data.json",
        passengers_data_path="test_data/passengers_data.json"
    )
    
    # Detect disruptions
    disruptions = detector.detect_all_disruptions()
    
    # Generate summary
    print("\n" + "="*80)
    print("DETECTION SUMMARY")
    print("="*80)
    
    summary = detector.generate_summary_report()
    
    print(f"\n📊 Total Disruptions: {summary['total_disruptions']}")
    print(f"👥 Total Passengers Affected: {summary['total_passengers_affected']}")
    print(f"⭐ High-Value Passengers: {summary['total_high_value_passengers']}")
    print(f"🔄 Connecting Passengers: {summary['total_connecting_passengers']}")
    print(f"\n💰 Total Estimated Cost Impact: ${summary['total_estimated_cost']:,.2f}")
    
    print(f"\n📋 Severity Breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        print(f"   {severity}: {count} flight(s)")
    
    print(f"\n🔧 Actions Required:")
    print(f"   Flights needing rebooking: {summary['flights_requiring_rebooking']}")
    print(f"   Flights needing accommodation: {summary['flights_requiring_accommodation']}")
    
    # Export results
    output_file = detector.export_disruptions()
    print(f"\n✅ Disruption data exported to: {output_file}")
    
    print("\n" + "="*80)
    print("✓ DETECTION COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
