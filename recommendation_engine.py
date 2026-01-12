"""
AI Decision Recommendation Engine
Generates rebooking, compensation, and communication options for disrupted flights and affected passengers
"""

import json
import requests
from typing import List, Dict
from datetime import datetime

class RecommendationEngine:
    """Engine to generate recommendations for disruptions"""
    def __init__(self, disruptions_path: str, flights_path: str = None, passengers_path: str = None, bookings_path: str = None, resources_path: str = None, disruption_events_path: str = None):
        with open(disruptions_path, 'r') as f:
            self.data = json.load(f)
        self.recommendations = []
        self.flights = []
        self.passengers = []
        self.bookings = []
        self.resources = []
        self.disruption_events = []
        if flights_path:
            with open(flights_path, 'r') as f:
                self.flights = json.load(f)
        if passengers_path:
            with open(passengers_path, 'r') as f:
                self.passengers = json.load(f)
        if bookings_path:
            with open(bookings_path, 'r') as f:
                self.bookings = json.load(f)
        if resources_path:
            with open(resources_path, 'r') as f:
                self.resources = json.load(f)
        if disruption_events_path:
            with open(disruption_events_path, 'r') as f:
                self.disruption_events = json.load(f)

    def generate_recommendations(self):
        for disruption in self.data['disruptions']:
            rec = self._recommend_for_disruption(disruption)
            self.recommendations.append(rec)
        return self.recommendations

    def _query_ollama(self, prompt: str, model: str = "llama2") -> str:
        """Sends a prompt to the Ollama API and returns the response."""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}},
                timeout=60
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error querying Ollama: {e}")
            return ""

    def _recommend_for_disruption(self, disruption: Dict) -> Dict:
        """Generates recommendations for a single disruption using Ollama."""
        # Prepare prompt for LLM with explicit instructions for JSON-only output
        json_schema = {
            "disruption_id": "string",
            "flight_number": "string",
            "flight_date": "string",
            "rebooking_options": [
                {"flight_number": "EY130", "new_departure_time": "2025-11-27T23:00:00", "new_arrival_time": "2025-11-28T07:00:00", "passenger_count": 100}
            ],
            "vouchers": [
                {"type": "meal", "amount": 50, "currency": "USD", "quantity": 100}
            ],
            "compensation": [
                {"type": "monetary", "amount": 400, "currency": "USD", "passenger_count": 100}
            ],
            "communications": [
                {"channel": "email", "recipient_group": "all_affected", "message_template": "Your flight has been disrupted. Compensation details: ..."}
            ],
            "operational_actions": [
                {"action": "arrange_transport", "details": "Bus from terminal to hotel"}
            ],
            "cost_optimization": [
                {"measure": "use_hotel_voucher_instead_of_cash", "estimated_saving": 5000, "currency": "USD"}
            ]
        }
        
        prompt = (
            "You are an airline disruption management assistant. Generate ONLY valid JSON output (no text before or after) based on this disruption. "
            f"Use this exact JSON schema: {json.dumps(json_schema)}. "
            "Return a JSON object with the same keys, adapting values for this disruption. "
            f"Disruption data: {json.dumps(disruption)}"
        )
        
        llm_output = self._query_ollama(prompt)

        if not llm_output:
            return self._fallback_recommendations(disruption)

        # Clean up the response from the LLM
        llm_output = llm_output.strip()
        
        # Find the first and last curly braces to extract JSON
        start = llm_output.find('{')
        end = llm_output.rfind('}')

        if start != -1 and end != -1 and end > start:
            candidate = llm_output[start:end+1]
            try:
                parsed = json.loads(candidate)
                # Verify it has the required keys
                if all(key in parsed for key in ["disruption_id", "flight_number", "flight_date"]):
                    return parsed
                else:
                    return self._fallback_recommendations(disruption)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}. Falling back to rule-based recommendations.")
                return self._fallback_recommendations(disruption)
        
        # If no valid JSON found, use fallback
        return self._fallback_recommendations(disruption)
    
    def _fallback_recommendations(self, disruption: Dict) -> Dict:
        """Rule-based fallback recommendations when LLM fails."""
        rebooking_options = []
        vouchers = []
        compensation = []
        communications = []
        operational_actions = []
        cost_optimization = []
        
        # Condition: Flight delayed >= 3 hours (180 min)
        if disruption.get('delay_minutes', 0) >= 180 and disruption.get('disruption_status') == 'Delayed':
            for pax in disruption.get('affected_passenger_list', [])[:5]:  # Limit to first 5 for demo
                vouchers.append({
                    "type": "meal",
                    "amount": 50,
                    "currency": "USD",
                    "quantity": 1
                })
        
        # Condition: Flight cancelled or rescheduled >= 24 hours (1440 min)
        if disruption.get('disruption_status') == 'Cancelled' or disruption.get('delay_minutes', 0) >= 1440:
            rebooking_options.append({
                "flight_number": "EY130",
                "new_departure_time": disruption.get('estimated_departure', ''),
                "new_arrival_time": disruption.get('estimated_arrival', ''),
                "passenger_count": len(disruption.get('affected_passenger_list', []))
            })
            compensation.append({
                "type": "monetary",
                "amount": 600,
                "currency": "USD",
                "passenger_count": len(disruption.get('affected_passenger_list', []))
            })
        
        # Default compensation
        if not compensation:
            compensation.append({
                "type": "monetary",
                "amount": 400,
                "currency": "USD",
                "passenger_count": len(disruption.get('affected_passenger_list', []))
            })
        
        # Communications
        communications.append({
            "channel": "email",
            "recipient_group": "all_affected",
            "message_template": f"Your flight {disruption.get('flight_number')} has been disrupted due to {disruption.get('disruption_reason')}. Compensation details will follow."
        })
        
        # Operational actions
        operational_actions.append({
            "action": "assign_ground_staff",
            "details": "Coordinate with ground services for passenger assistance"
        })
        
        # Cost optimization
        cost_optimization.append({
            "measure": "optimize_resource_allocation",
            "estimated_saving": 2000,
            "currency": "USD"
        })
        
        return {
            "disruption_id": disruption.get('disruption_id', 'UNKNOWN'),
            "flight_number": disruption.get('flight_number', 'UNKNOWN'),
            "flight_date": disruption.get('flight_date', 'UNKNOWN'),
            "rebooking_options": rebooking_options,
            "vouchers": vouchers,
            "compensation": compensation,
            "communications": communications,
            "operational_actions": operational_actions,
            "cost_optimization": cost_optimization,
            "source": "fallback_rule_based"
        }

    def export_recommendations(self, output_path: str = "recommendations.json"):
        data = {
            'generated_at': datetime.now().isoformat(),
            'recommendations': self.recommendations
        }
        # Always export to test_data folder
        output_path = "test_data/recommendations.json"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        return output_path

def main():
    print("="*80)
    print("AI DECISION RECOMMENDATION ENGINE - INITIALIZING")
    print("="*80)
    engine = RecommendationEngine(
        disruptions_path="test_data/detected_disruptions.json",
        flights_path="test_data/flights_data.json",
        passengers_path="test_data/passengers_data.json",
        bookings_path="test_data/bookings_data.json",
        resources_path="test_data/resources_data.json",
        disruption_events_path="test_data/disruption_events_data.json"
    )
    engine.generate_recommendations()
    output_file = engine.export_recommendations()
    print(f"\n✅ Recommendations exported to: {output_file}")
    print("="*80)

if __name__ == "__main__":
    main()
