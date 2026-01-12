# COMPLETE ELIGIBILITY RULES - AIRLINE DISRUPTION MANAGEMENT SYSTEM

## 1. DISRUPTION DETECTION RULES

### A. Primary Disruption Check
A passenger is considered **DISRUPTED** if ANY of these conditions are true:

#### Condition 1: Missed Connection (Priority)
```
IF passenger has connecting flight (next_segment_arrival_iataCode exists)
   AND arrival_delay >= Minimum_Connecting_Time(connection_airport)
   THEN passenger is DISRUPTED
```

**Minimum Connecting Time (MCT) by Airport:**
```
LHR (London Heathrow)     = 90 minutes
AUH (Abu Dhabi)           = 75 minutes
DXB (Dubai)               = 90 minutes
JFK (New York)            = 120 minutes
CDG (Paris)               = 90 minutes
LAX (Los Angeles)         = 120 minutes
SFO (San Francisco)       = 120 minutes
BOM (Mumbai)              = 60 minutes
DEL (Delhi)               = 60 minutes
CAI (Cairo)               = 60 minutes
SYD (Sydney)              = 120 minutes
JED (Jeddah)              = 60 minutes
MAD (Madrid)              = 90 minutes
```

Example: 
- Flight EY129 arrives LHR with 90-minute delay
- Passenger Michael Wilson has connection to London
- 90 >= 90 (MCT for LHR) → DISRUPTED ✅

#### Condition 2: Significant Arrival Delay (Fallback)
```
IF passenger has NO connecting flight
   AND arrival_delay > 60 minutes
   THEN passenger is DISRUPTED
```

Example:
- Flight EY200 arrives with 120-minute delay
- Passenger has no further connection
- 120 > 60 → DISRUPTED ✅

#### Condition 3: No Disruption
```
IF neither Condition 1 nor Condition 2 is met
   THEN passenger is NOT DISRUPTED
   THEN NO actions are eligible
```

Example:
- Flight arrives 45 minutes late
- No connection
- 45 < 60 → NOT DISRUPTED ❌
- All actions are disabled

---

## 2. ACTION ELIGIBILITY THRESHOLDS

Once a passenger is confirmed as DISRUPTED, eligibility for each action is determined:

### A. REBOOKING
```
Eligibility Rule: ALWAYS (if disrupted)
Threshold: 0 minutes (no delay required)
Reason: Core disruption recovery tool, fundamental right

Conditions:
✓ Passenger is disrupted
✓ Alternative flights exist
✓ Rebooking doesn't violate airline policy
```

**Example Scenarios:**
- 45 min delay, no connection → NOT disrupted → No rebooking ❌
- 90 min delay, has connection → Disrupted → YES rebooking ✅
- 30 min delay, has connection to LHR → NOT disrupted (30 < 90) → No rebooking ❌
- 120 min delay, has connection to LHR → Disrupted → YES rebooking ✅

---

### B. MEAL VOUCHER
```
Eligibility Rule: delay_minutes >= 120
Threshold: 2 hours
Regulation: IATA Standard
Reason: Passenger feeding obligation

Voucher Amount Varies by Ticket Class:
├─ Economy: $25 per meal
├─ Premium Economy: $35 per meal
├─ Business: $50 per meal
└─ First: $75 per meal

Quantity Based on Delay:
├─ 120-240 min: 1 meal
├─ 240-480 min: 2 meals
├─ 480+ min: 3 meals
```

**Example Calculations:**
- 90 min delay → NOT eligible ❌
- 120 min delay → 1 meal voucher ✅
  - Economy passenger: $25 × 1 = $25
  - Business passenger: $50 × 1 = $50
- 300 min delay → 2 meal vouchers ✅
  - Economy: $25 × 2 = $50
  - Business: $50 × 2 = $100
- 600 min delay → 3 meal vouchers ✅
  - Economy: $25 × 3 = $75
  - Business: $50 × 3 = $150

---

### C. COMPENSATION (Regulatory)
```
Eligibility Rule: delay_minutes >= 180
Threshold: 3 hours
Regulation: EU261 Regulation (European flights)
Regulation: Montreal Convention (International)

Base Compensation by Flight Distance & Class:
```

**EU261 Compensation Rules:**

| Flight Distance | Economy | Premium | Business | First |
|-----------------|---------|---------|----------|-------|
| < 1,500 km     | €125    | €188    | €250     | €400  |
| 1,500-3,500 km | €250    | €375    | €500     | €800  |
| > 3,500 km     | €400    | €600    | €800     | €1,280|

**Tier Multipliers (Additional):**
```
Platinum Tier: Base × 3.2 (VIP consideration)
Gold Tier:     Base × 2.0 (Loyalty reward)
Silver Tier:   Base × 1.5 (Premium service)
Guest Tier:    Base × 1.0 (Standard)
```

**Example Calculations:**
- 150 min delay → NOT eligible ❌ (< 180)
- 180 min delay, Economy → $125 × 1.0 = $125 ✅
- 180 min delay, Platinum → $125 × 3.2 = $400 ✅
- 180 min delay, Business, Gold → $500 × 2.0 = $1,000 ✅

**Conditions for Compensation:**
- Airline responsibility (not force majeure)
- Disruption was avoidable
- Passenger must make claim (agent initiates)
- Payment method: Cash, Credit Card, Bank Transfer, or Voucher

---

### D. HOTEL ACCOMMODATION
```
Eligibility Rule: delay_minutes >= 720
Threshold: 12 hours (overnight stay required)
Reason: Passenger rest and welfare

Hotel Selection Based on Ticket Class:
├─ Economy → Standard (Comfort Inn level)
├─ Premium Economy → Comfort (Premier Business Hotel level)
├─ Business → Premium (Luxury Suites level)
└─ First → Luxury (Grand Luxury Resort level)

Available Hotels:
├─ Comfort Inn Downtown (Standard - $89-119/night)
├─ Premier Business Hotel (Comfort - $129-189/night)
├─ Luxury Suites Express (Premium - $189-349/night)
└─ Grand Luxury Resort (Luxury - $299-599/night)
```

**Example Scenarios:**
- 500 min delay → NOT eligible ❌ (< 720)
- 720 min delay → Eligible ✅
  - Economy: Comfort Inn (Single: $89, Double: $109, Twin: $119)
  - Business: Luxury Suites (Double Deluxe: $189, Suite: $249)
  - First: Grand Luxury (Premium Suite: $299, Royal Suite: $399)
- 1,440 min delay (24 hours) → Eligible for 2 nights ✅

**Hotel Package Includes:**
- Room accommodation
- Breakfast (included or voucher)
- Ground transportation (airport transfers)
- Wi-Fi and business center access
- Lounge access (Business/First class)

---

### E. TRANSPORT/CONNECTION ASSISTANCE
```
Eligibility Rule: delay_minutes >= 720
Threshold: 12 hours (same as hotel)
Reason: Long delay requires multi-modal transportation

Services Included:
├─ Ground Transportation
│  ├─ Taxi service
│  ├─ Shuttle service
│  ├─ Rental car assistance
│  └─ Public transport vouchers
├─ Connection Assistance
│  ├─ Priority rebooking to next destination
│  ├─ Seat guarantees
│  ├─ Baggage through-check
│  └─ Connection protection
└─ Support Services
   ├─ Concierge (Business/First)
   ├─ Lounge access
   ├─ Communication assistance
   └─ Family accommodation (if applicable)
```

**Connection Risk Assessment:**
```
HIGH Risk: delay >= 180 min AND passenger has tight connection
├─ MCT at destination cannot be met
├─ Baggage may not transfer
├─ Priority rebooking essential
└─ Agent intervention required

MEDIUM Risk: delay 90-180 min AND passenger has connection
├─ MCT may be at risk
├─ Baggage transfer uncertain
├─ Rebooking may be needed
└─ Agent monitoring recommended

LOW Risk: delay < 90 min AND passenger has connection
├─ MCT likely manageable
├─ Standard connection procedures apply
├─ Rebooking if voluntary only
└─ Routine handling
```

**Example Scenarios:**
- 600 min delay, connection to Paris → NOT eligible ❌ (< 720)
- 720 min delay, connection to Paris → Eligible ✅
  - Taxi/shuttle arranged
  - Priority rebooking: Paris next available flight
  - Lounge access (class dependent)
  - Baggage guaranteed through-checked
- 1,080 min delay, tight connection → HIGH Risk ✅
  - Concierge handles complete rebooking
  - VIP lounge with shower facilities
  - Priority boarding on connection

---

## 3. PRIORITY LEVEL CALCULATION

The system assigns priority to determine urgency and service level:

### Priority Matrix
```
CRITICAL Priority (Highest Urgency):
├─ Delay > 240 minutes (4 hours) AND
│  └─ Any passenger tier
├─ OR Delay > 120 minutes AND
│  └─ Platinum OR Gold tier
├─ OR Any delay AND
│  └─ Special Service Request (SSR) present
└─ Management escalation required

HIGH Priority (Urgent):
├─ Delay >= 120 minutes AND
│  └─ Platinum or Gold tier
├─ OR Delay > 180 minutes AND
│  └─ Any tier
├─ OR Passenger has critical connection
└─ Fast-track processing recommended

MEDIUM Priority (Standard):
├─ Delay 60-120 minutes AND
│  └─ Non-Platinum tier
├─ OR Delay 120-180 minutes AND
│  └─ Silver or Guest tier
└─ Normal processing timeline

LOW Priority (Routine):
├─ Delay < 60 minutes
├─ OR No connection risk
├─ OR Passenger opted for future travel credit
└─ Standard service handling
```

### SSR (Special Service Request) Types
```
Medical:
├─ PRM (Persons with Reduced Mobility)
├─ DEF (Deaf/Hard of Hearing)
├─ BLD (Blind/Visually Impaired)
└─ Automatic HIGH priority

Family:
├─ UMNR (Unaccompanied Minor)
├─ INFT (Infant)
├─ CHLD (Child)
└─ Automatic HIGH priority (with parent)

Dietary:
├─ VGML (Vegetarian/Vegan)
├─ KOSHER
├─ HALAL
└─ Routine processing
```

---

## 4. TIER-BASED SERVICE DIFFERENTIATION

### PLATINUM TIER
```
Characteristics:
├─ 100,000+ annual miles
├─ Status: Elite/Executive
├─ Loyalty: Highest

Eligibility Enhancements:
├─ Compensation: Base × 3.2 multiplier
├─ Hotel: Luxury tier (Grand Luxury Resort)
├─ Meal: Premium amounts ($75 First, $50 Business)
├─ Special: Concierge service + lounge + upgrades
├─ Priority: Always HIGH or CRITICAL

AI Recommendation Style:
├─ "As an elite Platinum member..."
├─ Mention: Executive treatment, concierge, upgrades
├─ Offer: Cabin upgrade, suite accommodation, premium dining
├─ Tone: VIP, exclusive, personalized
```

### GOLD TIER
```
Characteristics:
├─ 50,000-99,999 annual miles
├─ Status: Gold/Premier
├─ Loyalty: High

Eligibility Enhancements:
├─ Compensation: Base × 2.0 multiplier
├─ Hotel: Premium tier (Luxury Suites Express)
├─ Meal: Enhanced amounts ($50 Business, $35 Premium Economy)
├─ Special: Lounge access + priority rebooking
├─ Priority: HIGH if delay >= 120 min

AI Recommendation Style:
├─ "As a valued Gold member..."
├─ Mention: Priority service, lounge access, loyalty benefits
├─ Offer: Lounge access, priority boarding, meal vouchers
├─ Tone: Premium, attentive, appreciative
```

### SILVER TIER
```
Characteristics:
├─ 10,000-49,999 annual miles
├─ Status: Silver/Member
├─ Loyalty: Moderate

Eligibility Enhancements:
├─ Compensation: Base × 1.5 multiplier
├─ Hotel: Comfort tier (Premier Business Hotel)
├─ Meal: Standard amounts ($40 Business, $25 Economy)
├─ Special: Basic lounge + standard rebooking
├─ Priority: MEDIUM if delay >= 120 min

AI Recommendation Style:
├─ "As a valued Silver member..."
├─ Mention: Priority rebooking, lounge access, support
├─ Offer: Meal vouchers, rebooking assistance
├─ Tone: Professional, supportive, helpful
```

### GUEST TIER
```
Characteristics:
├─ < 10,000 annual miles
├─ Status: Guest/Occasional Flyer
├─ Loyalty: Minimal

Eligibility Enhancements:
├─ Compensation: Base × 1.0 (no multiplier)
├─ Hotel: Standard tier (Comfort Inn)
├─ Meal: Base amounts ($25 Economy, $40 Business)
├─ Special: Standard rebooking
├─ Priority: Delay-dependent

AI Recommendation Style:
├─ "We understand your situation..."
├─ Mention: Support, assistance, availability
├─ Offer: Rebooking help, meal vouchers, compensation
├─ Tone: Helpful, service-oriented, reassuring
```

---

## 5. SPECIAL CIRCUMSTANCES & EXCEPTIONS

### Force Majeure (No Compensation)
```
Events:
├─ Severe weather (thunderstorm, snow, extreme winds)
├─ Volcanic ash cloud
├─ Security threat
├─ Air traffic control strike
├─ Military action
└─ Natural disaster

Eligibility Impact:
├─ Rebooking: YES (still needed)
├─ Meal/Hotel: YES (still eligible)
├─ Compensation: NO (airline not responsible)
├─ Connection: YES (still needed)
```

### Airline Responsibility (Full Compensation)
```
Causes:
├─ Mechanical failure (airline-maintained)
├─ Crew scheduling failure
├─ Overbooking
├─ Operational decision (consolidation)
├─ Lack of proper maintenance
└─ Ground handling error

Eligibility Impact:
├─ Rebooking: YES
├─ Meal/Hotel: YES
├─ Compensation: YES (full amount)
├─ Connection: YES
```

### Partial Responsibility (Reduced Compensation)
```
Examples:
├─ Pilot sudden illness (unexpected)
├─ Late connecting flight (previous leg disrupted)
├─ Passenger delay check-in (partial fault)
└─ Baggage handling error

Eligibility Impact:
├─ Rebooking: YES
├─ Meal/Hotel: YES
├─ Compensation: 50%-75% (negotiated)
├─ Connection: YES
```

---

## 6. SUMMARY TABLE

| Action | Threshold | Regulation | Tier Multiplier | Disabled For |
|--------|-----------|-----------|-----------------|--------------|
| **Rebooking** | 0 min | IATA | 1.0x | Non-disrupted passengers |
| **Meal** | 120 min | IATA | 1.0x | Short delays |
| **Compensation** | 180 min | EU261 | 1.0-3.2x | Very short delays |
| **Hotel** | 720 min | IATA | Class-based | Non-overnight disruptions |
| **Transport** | 720 min | IATA | Class-based | Short disruptions |

---

## 7. CONFIGURATION CONSTANTS (In Code)

```python
MINIMUM_CONNECTING_TIME = {
    'LHR': 90, 'AUH': 75, 'DXB': 90, 'JFK': 120,
    'CDG': 90, 'LAX': 120, 'SFO': 120, 'BOM': 60,
    'DEL': 60, 'CAI': 60, 'SYD': 120, 'JED': 60,
    'MAD': 90
}

DELAY_THRESHOLDS = {
    'short_meal': 120,           # 2 hours
    'medium_hotel': 720,         # 12 hours
    'high_compensation': 180     # 3 hours
}

TIER_COMPENSATION_MULTIPLIERS = {
    'Platinum': 3.2,
    'Gold': 2.0,
    'Silver': 1.5,
    'Guest': 1.0
}

TICKET_CLASS_MEAL_AMOUNTS = {
    'Economy': 25,
    'Premium Economy': 35,
    'Business': 50,
    'First': 75
}
```

