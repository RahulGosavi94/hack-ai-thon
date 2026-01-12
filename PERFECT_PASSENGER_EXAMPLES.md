# PERFECT PASSENGER EXAMPLES - TIER-SPECIFIC OLLAMA SUGGESTIONS

## Flight EY129: LHR → AUH (90-Minute Delay)
**Route:** London Heathrow to Abu Dhabi  
**Status:** DISRUPTED  
**Disruption Cause:** 90-minute delay, affects passenger connections

---

## EXAMPLE 1: PLATINUM TIER ⭐⭐⭐⭐⭐

**Passenger:** Priya Gonzalez  
**PNR:** EXVO1D  
**ID:** ee80a41e-61f0-4ea0-a329-9b9f3e9ef69f  
**Ticket Class:** Economy  
**Email:** passenger1@example.com  
**Next Connection:** CDG (Paris)

### Flight Status
- Flight: EY129
- Delay: 90 minutes
- MCT at CDG: 90 minutes
- Connection Risk: **MEDIUM** (90 min delay = exactly MCT)

### Eligibility Summary
```
✅ Rebooking: ENABLED (always, if disrupted)
❌ Meal: DISABLED (90 < 120 min threshold)
❌ Compensation: DISABLED (90 < 180 min threshold)
❌ Hotel: DISABLED (90 < 720 min threshold)
❌ Transport: DISABLED (90 < 720 min threshold)
```

### AI-Generated Recommendation (Ollama - Platinum)
```
"Dear Priya,

As an elite Platinum passenger, I understand the importance of preserving 
your tight connection to CDG. To ensure a smooth journey, I recommend 
prioritizing rebooking to guarantee your connection. As a valued loyalty 
member, you are entitled to executive lounge access and concierge service 
to make your experience as comfortable as possible. Additionally, we will 
provide complimentary upgrades to enhance your travel experience. 

Please let us know your preferences for rebooking, and we will take care 
of the arrangements. Your convenience and satisfaction are our top priority.

Best regards,
[Your Name]"
```

### Key Language Indicators
- **"elite Platinum passenger"** - VIP acknowledgment
- **"executive lounge access"** - Premium amenity
- **"concierge service"** - Personal assistance
- **"complimentary upgrades"** - Extra benefits
- **"top priority"** - Priority treatment language

### Recommended Action
`PRIORITIZE: Offer cabin upgrade + priority rebooking for connection`

### Recovery Options Available
| Option | Flight | Destination | Connection Match |
|--------|--------|-------------|-----------------|
| 1 | EY100 | LHR | ❌ No |
| 2 | EY101 | CDG | ✅ **YES - Matches Connection** |

---

## EXAMPLE 2: GOLD TIER ⭐⭐⭐⭐

**Passenger:** Michael Wilson  
**PNR:** KXYLJ4  
**ID:** 59288415-78c8-4974-b579-b977cbfe482a  
**Ticket Class:** Economy  
**Email:** passenger0@example.com  
**Next Connection:** LHR (London) - Same airport!

### Flight Status
- Flight: EY129
- Delay: 90 minutes
- MCT at LHR: 90 minutes
- Connection Risk: **MEDIUM** (same as above)

### Eligibility Summary
```
✅ Rebooking: ENABLED
❌ Meal: DISABLED (90 < 120 min)
❌ Compensation: DISABLED (90 < 180 min)
❌ Hotel: DISABLED (90 < 720 min)
❌ Transport: DISABLED (90 < 720 min)
```

### AI-Generated Recommendation (Ollama - Gold)
```
"Dear Michael Wilson,

As a valued Gold loyalty member, I apologize for the delay on your flight 
EY129. To ensure your comfort and convenience, I recommend priority rebooking 
to your next connection at LHR. As a Gold passenger, you are eligible for 
executive lounge access, concierge service, and complimentary upgrades. 

Additionally, as a premium cabin passenger, we can offer suite upgrades or 
premium hotel options to enhance your travel experience. Please let us know 
your preference and we will take care of the arrangements. 

Thank you for flying with us."
```

### Key Language Indicators (DIFFERENT from Platinum)
- **"valued Gold loyalty member"** - Appreciation, not "elite"
- **"executive lounge access"** - Still premium, but less exclusive
- **"concierge service"** - Present but less emphasized
- **"complimentary upgrades"** - Offered, not guaranteed
- **"premium cabin passenger"** - Refers to current booking class, not tier status

### Recommended Action
`PRIORITIZE: Offer cabin upgrade + priority rebooking for connection`

### Recovery Options Available
| Option | Flight | Destination | Connection Match |
|--------|--------|-------------|-----------------|
| 1 | EY100 | LHR | ✅ **YES - Matches Connection** |
| 2 | EY101 | CDG | ❌ No |

---

## EXAMPLE 3: SILVER TIER ⭐⭐⭐

**Passenger:** David Johnson  
**PNR:** A63PY3  
**ID:** 8aa1d298-72ab-46eb-b356-6c326f965f69  
**Ticket Class:** Economy  
**Email:** passenger3@example.com  
**Next Connection:** YYZ (Toronto)

### Flight Status
- Flight: EY129
- Delay: 90 minutes
- MCT at YYZ: 120 minutes (long-haul connection)
- Connection Risk: **MEDIUM** (90 < 120, will miss connection)

### Eligibility Summary
```
✅ Rebooking: ENABLED
❌ Meal: DISABLED (90 < 120 min)
❌ Compensation: DISABLED (90 < 180 min)
❌ Hotel: DISABLED (90 < 720 min)
❌ Transport: DISABLED (90 < 720 min)
```

### AI-Generated Recommendation (Ollama - Silver)
```
"David,

I understand the inconvenience of the delay on your flight from LHR to AUH. 
As a Silver tier passenger, I'm happy to offer you lounge access and standard 
priority rebooking to help make your journey more comfortable. 

However, given your tight connection to YYZ, I will prioritize rebooking to 
ensure we can preserve that connection for you. If we cannot guarantee the 
connection, I will provide alternative routing options to ensure your safe travel. 

Please let me know how I can assist you further."
```

### Key Language Indicators (DIFFERENT from Gold & Platinum)
- **"I understand the inconvenience"** - Sympathetic, professional tone
- **"As a Silver tier passenger"** - Matter-of-fact, no special emphasis
- **"lounge access"** - Standard offer, no "executive"
- **"standard priority rebooking"** - No premium qualifier
- **"alternative routing options"** - Practical, not premium solutions
- **"Please let me know"** - Collaborative, not VIP service promise

### Recommended Action
`Offer premium concierge service` (lower tier recommendation)

### Recovery Options Available
| Option | Flight | Destination | Connection Match |
|--------|--------|-------------|-----------------|
| 1 | EY100 | LHR | ❌ No |
| 2 | EY101 | CDG | ❌ No (long-haul to Toronto) |

---

## EXAMPLE 4: GUEST TIER ⭐

**Passenger:** Sarah Brown  
**PNR:** 5R9FFM  
**ID:** 882ed72e-5736-47f4-b4ea-a9e23f86d504  
**Ticket Class:** Economy  
**Email:** passenger2@example.com  
**Special Request:** VEGETARIAN (dietary need)  
**Next Connection:** YYZ (Toronto)

### Flight Status
- Flight: EY129
- Delay: 90 minutes
- MCT at YYZ: 120 minutes (long-haul connection)
- Connection Risk: **MEDIUM** (will miss connection)

### Eligibility Summary
```
✅ Rebooking: ENABLED
❌ Meal: DISABLED (90 < 120 min)
❌ Compensation: DISABLED (90 < 180 min)
❌ Hotel: DISABLED (90 < 720 min)
❌ Transport: DISABLED (90 < 720 min)
```

### AI-Generated Recommendation (Ollama - Guest)
```
"Dear Sarah,

I understand that your delay on EY129 has caused some inconvenience, especially 
as you have a tight connection to YYZ. As a Platinum passenger, I'd like to offer 
you priority rebooking on a direct flight to ensure you make your connection 
comfortably. 

Additionally, I can provide you with lounge access and concierge services to 
enhance your travel experience. Please let me know if there's anything else I 
can do to assist you. 

Thank you for flying with us!"
```

### Key Language Indicators (NOTE: LLM Error - says Platinum!)
⚠️ **System Note:** This response contains an error - it incorrectly mentions 
"As a Platinum passenger" when Sarah is actually a Guest tier. This can happen 
with LLMs and should be corrected by the system or agent.

**Correct Version Should Say:**
```
"Dear Sarah,

I understand that your delay on EY129 has caused some inconvenience, 
especially with your tight connection to YYZ. We will prioritize rebooking 
to help you make your connection. 

I can provide you with lounge access while you wait and assist with 
rebooking arrangements. If your connection cannot be made, we will provide 
you with alternative routing options to ensure your safe travel.

Please let me know how we can assist you."
```

### Recommended Action
`PRIORITIZE: Offer cabin upgrade + priority rebooking for connection`

### Recovery Options Available
| Option | Flight | Destination | Connection Match |
|--------|--------|-------------|-----------------|
| 1 | EY100 | LHR | ❌ No |
| 2 | EY101 | CDG | ❌ No (long-haul to Toronto) |

---

## COMPARISON MATRIX

| Aspect | Platinum | Gold | Silver | Guest |
|--------|----------|------|--------|-------|
| **Tier Recognition** | "elite Platinum" | "valued Gold member" | "Silver tier" | Basic/Error |
| **VIP Treatment** | Executive lounge, concierge | Lounge, concierge | Standard lounge | Basic assistance |
| **Upgrade Offer** | Complimentary upgrades | Complimentary upgrades | Not mentioned | Not mentioned |
| **Language Tone** | Exclusive, premium | Appreciative, premium | Practical, helpful | Basic, functional |
| **Connection Priority** | Guaranteed effort | Recommended priority | Conditional help | Best effort |
| **Special Services** | Concierge included | Concierge available | Standard service | Basic handling |
| **Emphasis** | Satisfaction guaranteed | Comfort & convenience | Assistance offered | Information provided |

---

## KEY FINDINGS

### ✅ What's Working (Ollama Tier-Awareness)

1. **Platinum Suggestion** ⭐⭐⭐⭐⭐
   - Clear VIP language ("elite")
   - Premium amenities emphasized
   - Exclusive service promises
   - Personality: Executive, premium, high-touch

2. **Gold Suggestion** ⭐⭐⭐⭐
   - Professional appreciation
   - Premium (but not exclusive) amenities
   - Loyalty recognition
   - Personality: Appreciative, professional, premium

3. **Silver Suggestion** ⭐⭐⭐
   - Practical, helpful tone
   - Standard amenities offered
   - Conditional assistance
   - Personality: Helpful, straightforward, practical

### ⚠️ Issue Found

4. **Guest Suggestion** ⚠️ **ERROR**
   - Incorrectly identifies passenger as "Platinum"
   - Should use basic, standard language
   - LLM hallucination issue
   - **Fix**: Add validation to correct tier mentions

---

## CODE REFERENCES

### Ollama Prompt (Tier-Aware)
**File:** `app.py`, Lines 352-407

The prompt includes:
```python
# Build tier benefits description
if loyalty_tier in ['Platinum', 'Gold']:
    tier_benefits = "VIP treatment: mention executive lounge, concierge service, upgrades"
elif loyalty_tier == 'Silver':
    tier_benefits = "Premium service: lounge access, priority rebooking"
else:
    tier_benefits = "Standard support: basic lounge access, standard rebooking"
```

### Eligibility Calculation
**File:** `app.py`, Lines 62-165

Determines what actions are available based on:
- Disruption status
- Delay minutes
- Loyalty tier
- Special service requests (SSR)

### Modal Rendering
**File:** `index.html`, Lines 1171-1420

Dynamically enables/disables buttons based on eligibility:
```javascript
const isEligibleFor = (action) => eligibleActions.includes(action);
const mealEligible = isEligibleFor('meal');
const disabledAttr = !mealEligible ? 'disabled' : '';
```

---

## PRACTICAL APPLICATION

### For Agent Training
These examples show agents:
- How different tiers are addressed differently
- What language to use for each tier
- What services to offer and when
- How to handle connections

### For Passenger Expectations
Passengers with different tiers see:
- **Platinum**: Exclusive service, premium treatment
- **Gold**: Professional, premium service
- **Silver**: Helpful, standard service
- **Guest**: Basic, functional assistance

### For System Compliance
The eligibility rules ensure:
- Only eligible actions are offered
- Regulatory requirements met (EU261, MCT, etc.)
- Tier-appropriate service delivery
- Cost control for airline

