# 📸 System Screenshots & Tab Documentation

Complete visual documentation of all application tabs with descriptions, data samples, and usage examples.

---

## 📑 Table of Contents

1. [Flight List Tab](#1-flight-list-tab)
2. [Passengers Tab](#2-passengers-tab)
3. [Manager Summary Tab](#3-manager-summary-tab)
4. [Disruptions Tab](#4-disruptions-tab)
5. [Recommendations Tab](#5-recommendations-tab)
6. [Using the Application](#using-the-application)
7. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## 1️⃣ Flight List Tab

### 📌 Overview

The **Flight List** tab provides real-time monitoring of all flights in the system with disruption status indicators and quick access to detailed information.

### 🎯 Purpose

- Track all flights at a glance
- Quickly identify disrupted flights
- Access detailed disruption information
- Monitor flight status changes

### 📊 Data Displayed

| Column | Description | Example |
|--------|-------------|---------|
| Flight Number | Unique flight identifier | EY234 |
| Airline | Operating airline name | Etihad Airways |
| Route | Departure → Arrival | DXB → LHR |
| Scheduled Departure | Original departure time | 2024-01-15 08:00 |
| Status | Current flight status | Delayed / On-Time |
| Passengers | Total passengers on flight | 250 |
| Actions | View details link | View Details |

### 🔴 Flight Status Indicators

| Status | Color | Meaning | Action |
|--------|-------|---------|--------|
| ✅ On-Time | Green | Flight operating normally | None required |
| ⚠️ Delayed | Red | Flight delayed | View disruption details |
| ❌ Cancelled | Red | Flight cancelled | Full care required |
| 🔄 Diverted | Red | Alternate airport | Full care required |

### 📋 Sample Data

**Flight: EY234**
- Airline: Etihad Airways
- Route: Dubai (DXB) → London Heathrow (LHR)
- Scheduled Departure: 2024-01-15 08:00 AM
- Status: **Delayed** (2.5 hours)
- Total Passengers: 250
- Disruption: YES → View Details available

**Flight: EY789**
- Airline: Etihad Airways
- Route: Dubai (DXB) → Frankfurt (FRA)
- Scheduled Departure: 2024-01-15 11:30 AM
- Status: **On-Time** (green)
- Total Passengers: 280
- Disruption: NO → No action needed

### ✨ Features

- ✅ Real-time status updates
- ✅ Color-coded status indicators
- ✅ Quick disruption access
- ✅ Responsive layout
- ✅ Sort by status or time
- ✅ Search functionality

### 🔗 Interactions

1. **View Disruption Details**
   - Click "View Details" button on any disrupted flight
   - Navigates to Disruptions tab with flight filtered
   - Shows affected passengers and care options

2. **Monitor Status Changes**
   - Page auto-refreshes every 30 seconds
   - Visual status changes immediately visible
   - Notifications for status changes (if enabled)

3. **Filter Flights**
   - Filter by status (On-Time/Delayed/Cancelled/Diverted)
   - Filter by airline
   - Filter by route

### 💡 Usage Tips

- **For Operations Teams:** Monitor all flights for disruptions
- **For Management:** Get quick overview of disruption count
- **For Passengers:** Check your flight status
- **For Agents:** Access flight details quickly

### 📱 Responsive Design

- Desktop: Full table view with all columns
- Tablet: Condensed view with essential columns
- Mobile: Card-based layout with swipe navigation

---

## 2️⃣ Passengers Tab

### 📌 Overview

The **Passengers** tab provides comprehensive management of disrupted passengers with powerful search, filtering, and communication capabilities.

### 🎯 Purpose

- Manage disrupted passenger information
- Search and locate specific passengers
- View eligibility status and tier assignment
- Access passenger communication preferences
- Track passenger care actions

### 👥 Data Displayed

| Field | Description | Example |
|-------|-------------|---------|
| Passenger Name | Full name of passenger | John Doe |
| PNR | Passenger Name Record | ABC123 |
| Booking Reference | Booking confirmation | ABC123XYZ |
| Flight | Associated disrupted flight | EY234 |
| Tier | Care tier assignment | Gold |
| Eligible | Eligibility status | Yes / No |
| Ticket Price | Original ticket cost | $1,200 |
| Seat Class | Cabin class booked | Business / Economy |
| Email | Contact email | john@example.com |
| Phone | Contact phone | +1-555-0100 |

### 🏆 Passenger Tiers

#### 🥇 Gold Tier (40 passengers)
- High-value passengers (ticket > $1,000)
- Premium loyalty status
- Priority care and rebooking
- Premium lounge access
- Hotel accommodation (5+ hour disruption)
- Special meal vouchers

#### 🥈 Silver Tier (60 passengers)
- Standard passengers (ticket $500-$1,000)
- Standard loyalty status
- Standard rebooking process
- Meal vouchers ($25-30)
- Lounge access
- Communication priority

#### 🥉 Bronze Tier (50 passengers)
- Budget passengers (ticket < $500)
- No loyalty status
- Basic care offered
- Meal vouchers ($15-20)
- Self-service rebooking available
- Standard communication

### 🔍 Search & Filter Features

#### Search by Name
```
Search: "John"
Results: All passengers with "John" in name
Example: John Doe, John Smith, Johnson, etc.
```

#### Search by PNR
```
Search: "ABC123"
Results: Exact match for PNR ABC123
Returns: Single or multiple records per PNR
```

#### Filter by Tier
```
Select: "Gold"
Results: 40 gold-tier passengers
Shows: Premium care passengers only
```

#### Filter by Eligibility
```
Select: "Eligible"
Results: ~120 eligible passengers
Shows: Customers who qualify for care
```

#### Filter by Flight
```
Select: "EY234"
Results: All passengers on flight EY234
Count: ~250 passengers
```

### 📋 Sample Passenger Records

**Passenger Record 1 - Gold Tier**
- Name: John Doe
- PNR: ABC123
- Booking Reference: ABC123XYZ
- Flight: EY234 (Delayed 2.5 hours)
- Tier: **Gold**
- Eligible: **YES**
- Ticket Price: $1,500 (Business)
- Loyalty: Gold Member (50,000 miles)
- Email: john.doe@corporate.com
- Phone: +1-555-0123
- Care Actions: Premium rebook, upgrade offered, hotel booked

**Passenger Record 2 - Silver Tier**
- Name: Jane Smith
- PNR: XYZ789
- Booking Reference: XYZ789ABC
- Flight: EY456 (Cancelled)
- Tier: **Silver**
- Eligible: **YES**
- Ticket Price: $750 (Economy)
- Loyalty: Silver Member (10,000 miles)
- Email: jane.smith@email.com
- Phone: +1-555-0456
- Care Actions: Standard rebook, meal voucher $30

**Passenger Record 3 - Bronze Tier**
- Name: Bob Wilson
- PNR: QWE456
- Booking Reference: QWE456RST
- Flight: EY678 (Delayed 1.5 hours)
- Tier: **Bronze**
- Eligible: **NO** (Delay < 2 hours)
- Ticket Price: $299 (Economy)
- Loyalty: None
- Email: bob.wilson@email.com
- Phone: +1-555-0789
- Care Actions: Self-service rebooking available

### ✨ Features

- ✅ Advanced search (name, PNR, email)
- ✅ Multi-filter capabilities
- ✅ Real-time eligibility display
- ✅ Tier-based highlighting
- ✅ Contact information visible
- ✅ Communication preferences
- ✅ Care action tracking
- ✅ Bulk operations (export, notify)

### 🔗 Interactions

1. **Search Passenger**
   - Type name or PNR in search box
   - Real-time filtering as you type
   - View all matching passengers
   - Click passenger to view details

2. **Filter by Tier**
   - Select tier from dropdown
   - View all passengers in that tier
   - Shows tier-specific care options
   - Quick mass actions per tier

3. **View Passenger Details**
   - Click passenger name or row
   - Shows full profile
   - Communication history
   - Care action log
   - Eligibility details

4. **Perform Care Actions**
   - From detail view, select action
   - Rebook on alternative flight
   - Issue vouchers
   - Send notifications
   - Log interaction

### 💡 Usage Tips

**For Customer Service:**
- Search by name to locate passengers quickly
- View eligibility status before offering care
- Filter by tier to handle Gold passengers first

**For Rebooking Teams:**
- Sort by connection time for priority rebooking
- Filter eligible passengers only
- Bulk assign to agents

**For Finance:**
- Export passenger list with prices
- Filter by tier to calculate costs
- Track voucher issuance per tier

**For Management:**
- View disruption impact by tier
- Monitor care action completion
- Track passenger satisfaction

### 📱 Display Options

- **List View:** Full table with sorting
- **Card View:** Individual cards with key info
- **Map View:** Passenger distribution by location
- **Export:** CSV, PDF, Excel formats

---

## 3️⃣ Manager Summary Tab

### 📌 Overview

The **Manager Summary** tab is an executive-level dashboard providing KPI metrics, trend analysis, and disruption insights at a glance.

### 🎯 Purpose

- Monitor high-level KPI metrics
- Track disruption impact
- Measure passenger care effectiveness
- Identify cost drivers
- Support decision-making

### 📊 Key Performance Indicators (KPIs)

#### 1. 👥 Total Disrupted Passengers
- **Metric:** 150
- **Meaning:** Total passengers affected by current disruptions
- **Trend:** ↑ 15% from yesterday
- **Action:** Monitor growth if continuing to increase

#### 2. 💰 Total Disrupted Passenger Value
- **Metric:** $257,350
- **Meaning:** Total ticket value of disrupted passengers
- **Breakdown:**
  - Gold Tier: $60,000 (40 passengers × $1,500 avg)
  - Silver Tier: $45,000 (60 passengers × $750 avg)
  - Bronze Tier: $14,950 (50 passengers × $299 avg)
- **Impact:** Significant financial exposure

#### 3. 🎁 Vouchers Issued
- **Metric:** 30 (20% of eligible passengers)
- **Value:** $15,000 total
- **Average per Passenger:** $500
- **Breakdown by Tier:**
  - Gold: $12,000 (24 passengers × $500)
  - Silver: $2,400 (6 passengers × $400)
  - Bronze: $600 (1 passenger × $600)

#### 4. ✈️ Passengers Reprotected
- **Metric:** 40 (26.7% of disrupted passengers)
- **Meaning:** Successfully rebooked on alternative flights
- **Alternative Flight Success Rate:** 85%
- **Average Rebooking Time:** 2.3 hours
- **Breakdown:**
  - Same Day: 35 passengers
  - Next Day: 5 passengers

### 📈 Disruption Metrics

| Metric | Value | Trend |
|--------|-------|-------|
| Total Disruptions | 7 | Stable |
| Average Duration | 2.3 hours | ↓ 10% |
| Most Common Type | Delayed (4) | Up |
| Least Common Type | Diverted (1) | Down |
| Total Affected Passengers | 1,750 | ↑ 5% |

### 🏆 Tier Distribution

```
Disrupted Passengers by Tier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gold:   ████████████░░░░░░░░ 40 (26.7%)
Silver: █████████████████░░░ 60 (40.0%)
Bronze: ████████████░░░░░░░░ 50 (33.3%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total:                      150 passengers
```

### 💹 Financial Impact Analysis

| Category | Amount | % of Total |
|----------|--------|-----------|
| Original Ticket Value | $257,350 | 100% |
| Vouchers Issued | $15,000 | 5.8% |
| Hotel Costs (estimated) | $18,000 | 7.0% |
| Rebooking Costs | $8,000 | 3.1% |
| **Total Cost** | **$41,000** | **15.9%** |

### ✨ Dashboard Features

- ✅ Real-time KPI updates
- ✅ Trend indicators (up/down arrows)
- ✅ Tier-based breakdowns
- ✅ Cost analysis charts
- ✅ Recovery metrics
- ✅ Comparative analysis (vs. period)
- ✅ Forecasting (estimated costs)
- ✅ Export reports

### 📊 Chart Types

1. **Pie Chart:** Tier distribution
2. **Bar Chart:** Disruptions by type
3. **Line Chart:** Disruption trends over time
4. **Gauge Chart:** Recovery rate progress
5. **Heat Map:** Peak disruption hours

### 🔗 Drill-Down Navigation

- Click on "150 Passengers" → Go to Passengers tab
- Click on "7 Disruptions" → Go to Disruptions tab
- Click on "Gold Tier (40)" → Filter passengers by tier
- Click on "Delayed (4)" → Filter disruptions by type

### 💡 Usage Tips

**For Executives:**
- Review morning dashboard for overnight disruptions
- Track trends over time
- Monitor cost implications

**For Operations:**
- Focus on "Passengers Reprotected" metric
- Monitor average recovery time
- Identify bottlenecks

**For Finance:**
- Track total cost exposure
- Monitor voucher issuance
- Calculate cost per passenger

**For Quality Assurance:**
- Monitor passenger care metrics
- Track eligibility compliance
- Identify improvement areas

### 📋 Sample Dashboard View

```
╔════════════════════════════════════════════════════════════╗
║        MANAGER SUMMARY DASHBOARD                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Total Disrupted Passengers   150  ↑ 15%                 ║
║  Total Disrupted Value        $257.4K  ↑ 8%              ║
║  Vouchers Issued              30 ($15K)  ↓ 5%             ║
║  Passengers Reprotected       40 (26.7%) → View           ║
║                                                            ║
║  ┌──────────────────────────────────────────────────────┐ ║
║  │ Disruption Timeline (Last 24 Hours)                 │ ║
║  │ ▁▂▃▄▅▆▇██▇▆▅▄▂▁▁▂▃▄▅▄▃▂▁                           │ ║
║  └──────────────────────────────────────────────────────┘ ║
║                                                            ║
║  Tier Distribution:                                        ║
║  ▓▓▓▓▓▓▓▓░░ Gold (40) | ▓▓▓▓▓▓▓▓▓░ Silver (60)          ║
║  ▓▓▓▓▓▓░░░░ Bronze (50)                                  ║
║                                                            ║
║  Disruption Types:                                         ║
║  Delayed (4) | Cancelled (2) | Diverted (1)              ║
║                                                            ║
║  Cost Breakdown:                                           ║
║  Tickets: $257K | Vouchers: $15K | Hotels: $18K         ║
║  Estimated Total Cost: $41K (15.9% of ticket value)     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 4️⃣ Disruptions Tab

### 📌 Overview

The **Disruptions** tab displays detailed information about all flight disruptions with affected passenger counts, tier distribution, and care options.

### 🎯 Purpose

- View all active disruptions
- Analyze disruption details
- See affected passengers by tier
- Track disruption resolution
- Plan passenger care response

### 📋 Sample Disruptions

#### Disruption 1: EY234 Delayed

**Flight Information:**
- Flight Number: EY234
- Airline: Etihad Airways
- Route: Dubai (DXB) → London (LHR)
- Aircraft: Boeing 777-300ER

**Disruption Details:**
- Type: **Delayed**
- Duration: 2.5 hours
- Root Cause: Weather conditions at destination
- Description: Thunderstorm over London Heathrow
- Status: Ongoing (Estimated recovery 2:30 PM)

**Affected Passengers:**
- Total: 250
- Breakdown:
  - Gold (40): Premium care required
  - Silver (60): Standard care
  - Bronze (150): Basic care or self-service

**Care Actions Activated:**
- Premium rebooking offered to Gold passengers
- Hotel accommodation provided (5+ hours)
- Meal vouchers issued ($50-75)
- Lounge access granted
- Alternative flight arrangements begun

---

#### Disruption 2: EY456 Cancelled

**Flight Information:**
- Flight Number: EY456
- Airline: Etihad Airways
- Route: Dubai (DXB) → Paris (CDG)
- Aircraft: Airbus A380

**Disruption Details:**
- Type: **Cancelled**
- Root Cause: Technical maintenance issue
- Description: Aircraft unserviceable - replacement not available today
- Status: Resolved (Next flight next day)

**Affected Passengers:**
- Total: 280
- Breakdown:
  - Gold (50): Full premium care
  - Silver (100): Full standard care
  - Bronze (130): Full basic care

**Care Actions Required:**
- All passengers need rebooking
- Hotels mandatory for all (overnight disruption)
- Meal vouchers for all
- Ground transportation covered
- Tier-based additional care

---

#### Disruption 3: EY678 Delayed

**Flight Information:**
- Flight Number: EY678
- Airline: Etihad Airways
- Route: Dubai (DXB) → Frankfurt (FRA)
- Aircraft: Boeing 787

**Disruption Details:**
- Type: **Delayed**
- Duration: 1.5 hours
- Root Cause: Crew availability (flight crew delayed from previous flight)
- Description: Incoming crew delayed - scheduled to arrive 2:00 PM
- Status: Ongoing

**Affected Passengers:**
- Total: 220
- Note: Many passengers may not qualify for care (delay < 2 hours)

---

### 📊 Disruption Statistics

| Metric | Value |
|--------|-------|
| Total Disruptions | 7 |
| Delayed Flights | 4 (2-5 hours) |
| Cancelled Flights | 2 (full day) |
| Diverted Flights | 1 (alternate landing) |
| Total Affected | 1,750 passengers |
| Average Duration | 2.3 hours |

### 🏷️ Disruption Types

#### ⏰ Delayed
- **What:** Flight departure delayed beyond scheduled time
- **Duration:** Typically 1-24 hours
- **Care Trigger:** Usually > 2 hours
- **Examples:** Weather, crew, mechanical
- **Sample Duration:** EY234 (2.5 hrs), EY678 (1.5 hrs)

#### ❌ Cancelled
- **What:** Flight completely cancelled
- **Duration:** Affects entire day or longer
- **Care Trigger:** Always qualifies
- **Examples:** Weather, mechanical, crew shortage
- **Sample:** EY456 (cancelled, next day available)

#### 🔄 Diverted
- **What:** Flight lands at alternate airport
- **Duration:** 2-6 hours additional journey
- **Care Trigger:** Always qualifies
- **Example:** EY333 (diverted to alternate airport)

### ✨ Features

- ✅ Detailed disruption information
- ✅ Affected passenger breakdown by tier
- ✅ Root cause documentation
- ✅ Recovery timeline
- ✅ Care action tracking
- ✅ Historical records
- ✅ Duplicate disruption prevention
- ✅ Audit trail

### 🔗 Interactions

1. **View Disruption Details**
   - Click disruption card to expand
   - See full passenger breakdown
   - View care actions taken
   - Check recovery status

2. **Drill Down to Passengers**
   - Click "View Affected Passengers"
   - Filtered passenger list appears
   - Ready for mass actions
   - Communication available

3. **Take Care Actions**
   - Select passengers by tier
   - Assign rebooking
   - Issue vouchers
   - Send notifications
   - Log interactions

4. **Track Resolution**
   - Monitor recovery time
   - Update status
   - Mark as resolved
   - Archive disruption

---

## 5️⃣ Recommendations Tab

### 📌 Overview

The **Recommendations** tab displays AI-powered passenger care recommendations generated by Ollama LLM, with tier-based prioritization and actionable suggestions.

### 🎯 Purpose

- View AI-generated care recommendations
- Prioritize by tier (Gold → Silver → Bronze)
- Take actionable next steps
- Track recommendation completion
- Improve passenger satisfaction

### 🤖 AI Recommendation System

**Technology Stack:**
- **LLM:** Ollama (mistral, neural-chat, or other models)
- **Integration:** Flask API wrapper
- **Processing:** Real-time generation
- **Context:** Full passenger + flight + disruption data

**Recommendation Process:**
1. Analyze passenger profile (tier, ticket price, loyalty)
2. Consider disruption severity (type, duration)
3. Evaluate disruption rules (100+ rules)
4. Generate recommendations via Ollama
5. Score by priority and feasibility
6. Present actionable suggestions

### 🥇 Gold Tier Recommendations (40 passengers)

**Example 1: John Doe**
```
Passenger: John Doe (P001)
Flight: EY234 (Delayed 2.5 hours)
Ticket: $1,500 (Business)
Tier: Gold

RECOMMENDATION:
"Rebook passenger John Doe on next available premium cabin 
flight with complimentary upgrade to first class. Provide 
hotel accommodation for 5+ hour disruption, complimentary 
lounge access, and meal vouchers ($75). Offer travel 
insurance coverage and priority rebooking assistance."

ACTIONS:
✓ Premium rebook (next available flight)
✓ Upgrade to first class (complimentary)
✓ Hotel accommodation (5-star, 1 night)
✓ Meal vouchers ($75)
✓ Lounge access (Etihad Lounge)
✓ Travel insurance
✓ Priority phone support

PRIORITY: HIGH
ESTIMATED COST: $2,500
PASSENGER SATISFACTION IMPACT: Very High
```

**Example 2: Sarah Johnson**
```
Passenger: Sarah Johnson (P015)
Flight: EY456 (Cancelled)
Ticket: $1,800 (First Class)
Tier: Gold

RECOMMENDATION:
"Passenger Sarah Johnson must be rebooked on next available 
first-class flight within 24 hours. Provide 5-star hotel with 
amenities, spa access, premium car service to/from hotel, 
comprehensive meal allowance ($150), and personal rebooking 
assistant. Consider status match on partner airlines if 
rebooking not available same day."

ACTIONS:
✓ First-class rebook (next available, <24 hrs)
✓ 5-star hotel (premium room)
✓ Spa/wellness credit ($200)
✓ Premium car service (both directions)
✓ Meal allowance ($150)
✓ Personal assistant (dedicated)
✓ Status match on partners
✓ Complimentary lounge day pass

PRIORITY: CRITICAL
ESTIMATED COST: $3,500
PASSENGER SATISFACTION IMPACT: Exceptional
```

### 🥈 Silver Tier Recommendations (60 passengers)

**Example 3: Mike Chen**
```
Passenger: Mike Chen (P045)
Flight: EY234 (Delayed 2.5 hours)
Ticket: $750 (Economy)
Tier: Silver

RECOMMENDATION:
"Rebook passenger Mike Chen on next available flight with 
confirmed seat. Provide meal and refreshment vouchers 
($30-40), standard lounge access, and communication priority 
for any further changes. Monitor for any additional delays."

ACTIONS:
✓ Standard rebook (next available)
✓ Meal vouchers ($35)
✓ Lounge access (standard)
✓ Communication priority
✓ Rebooking confirmation
✓ Follow-up call within 2 hours

PRIORITY: MEDIUM
ESTIMATED COST: $200
PASSENGER SATISFACTION IMPACT: High
```

### 🥉 Bronze Tier Recommendations (50 passengers)

**Example 4: Tom Anderson**
```
Passenger: Tom Anderson (P120)
Flight: EY678 (Delayed 1.5 hours)
Ticket: $299 (Economy)
Tier: Bronze

NOTE: Passenger may not qualify for care (delay < 2 hours)

RECOMMENDATION:
"Passenger Tom Anderson is just below care qualification 
threshold. If delay extends beyond 2 hours, activate care. 
In the meantime, offer self-service rebooking option via 
mobile app or phone hotline. Provide refresh voucher ($15) 
as gesture of goodwill. Monitor for delay progression."

ACTIONS:
○ Monitor delay progression
○ Self-service rebooking available
○ Refresh voucher ($15) offered
○ Phone hotline available
○ Activate care if delay > 2 hours

PRIORITY: LOW
ESTIMATED COST: $15
PASSENGER SATISFACTION IMPACT: Medium
```

### 📊 Recommendation Statistics

| Metric | Value |
|--------|-------|
| Total Recommendations | 150 |
| Gold Tier | 40 (26.7%) |
| Silver Tier | 60 (40%) |
| Bronze Tier | 50 (33.3%) |
| Average Cost per Passenger | $271.67 |
| Total Estimated Cost | $40,750 |

### 🏷️ Recommendation Priorities

**🔴 CRITICAL** (< 1 hour)
- Cancelled flights
- Full-day disruptions
- Gold tier passengers
- Multiple connections at risk
- Examples: Immediate rebooking, hotel booking

**🟠 HIGH** (1-4 hours)
- Delayed flights (2-5 hours)
- Gold/Silver tier passengers
- Meal and voucher arrangements
- Lounge access
- Examples: Standard rebooking, meal vouchers

**🟡 MEDIUM** (4+ hours)
- Minor delays (< 2 hours)
- Silver/Bronze tier passengers
- Flexible care options
- Self-service available
- Examples: Information, options provided

**🟢 LOW** (monitoring)
- Minimal disruption
- Bronze tier passengers
- No immediate action
- Self-service enabled
- Examples: Monitor only, offer assistance

### 💡 Recommendation Actions

**Premium Rebooking:**
- Next available premium cabin flight
- Confirmed seat guaranteed
- Complimentary upgrade option
- < 24 hour rebooking

**Standard Rebooking:**
- Next available flight (same class)
- Confirmed seat guaranteed
- < 24 hour rebooking
- Standby options if needed

**Accommodation:**
- Hotel quality by tier
- Duration based on disruption
- Meals and transportation included
- Early check-in/late check-out

**Meal Vouchers:**
- Gold: $50-75 per meal
- Silver: $25-40 per meal
- Bronze: $15-20 per meal
- Multiple meals for long disruptions

**Lounge Access:**
- Gold: Premium lounge + amenities
- Silver: Standard lounge access
- Bronze: Not included (can offer)
- Duration: Full disruption period

### ✨ Features

- ✅ AI-powered recommendations
- ✅ Tier-based prioritization
- ✅ Actionable next steps
- ✅ Cost estimation
- ✅ Priority flagging
- ✅ Filter by tier
- ✅ Sort by priority
- ✅ Bulk actions
- ✅ Export recommendations
- ✅ Feedback collection

### 🔗 Interactions

1. **View Recommendation**
   - Click recommendation card
   - See full details and context
   - Review suggested actions
   - Check cost estimation

2. **Filter by Tier**
   - Select "Gold" to see 40 gold recommendations
   - Select "Silver" to see 60 silver recommendations
   - Select "Bronze" to see 50 bronze recommendations
   - Quick tier-based work assignment

3. **Take Action**
   - Click "Accept Recommendation"
   - Assign to agent
   - Track implementation
   - Mark as complete

4. **Provide Feedback**
   - Rate recommendation quality
   - Note if passenger accepted
   - Log actual cost vs. estimate
   - Improve future recommendations

---

## Using the Application

### 🚀 Getting Started

1. **Open Application**
   - Navigate to `http://localhost:5000`
   - Wait for page to load (2-3 seconds)

2. **Navigate Tabs**
   - Click tab names in top navigation
   - Tab content loads dynamically
   - Smooth transitions between tabs

3. **View Data**
   - Browse data in each tab
   - Click on items for details
   - Use filters and search

### 🔍 Searching & Filtering

**Flight List Tab:**
- Filter by status (On-Time, Delayed, etc.)
- Search by flight number
- Sort by time or airline

**Passengers Tab:**
- Search by name or PNR
- Filter by tier
- Filter by eligibility
- Sort by various columns

**Manager Summary Tab:**
- No search (dashboard only)
- Click KPIs to drill down
- View trends and charts

**Disruptions Tab:**
- Filter by disruption type
- Search by flight number
- Sort by duration or passengers

**Recommendations Tab:**
- Filter by tier
- Filter by priority
- Search by passenger name
- Sort by priority or cost

### 🖱️ Common Actions

**View Details:**
- Click "View Details" button
- Navigate to related tab
- Drill down to specific data

**Take Action:**
- Select checkboxes
- Click action button
- Confirm action
- See results

**Export Data:**
- Select data range
- Click "Export" button
- Choose format (CSV, PDF)
- Download file

**Refresh Data:**
- Click refresh button
- Page reloads latest data
- Automatic refresh: 30 seconds

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Next tab |
| `Shift + Tab` | Previous tab |
| `Ctrl + F` | Search (focus search box) |
| `Ctrl + P` | Print (current view) |
| `Escape` | Close modal/popup |
| `Enter` | Submit form |
| `R` | Refresh page |
| `?` | Show help |

---

## 📞 Need Help?

- **Questions:** Check [Documentation Index](DOCUMENTATION_INDEX.md)
- **Issues:** [GitHub Issues](https://github.com/RahulGosavi94/hack-ai-thon/issues)
- **Discussions:** [GitHub Discussions](https://github.com/RahulGosavi94/hack-ai-thon/discussions)

---

**Last Updated:** January 12, 2026  
**Version:** 1.0.0  
**Status:** Complete Documentation
