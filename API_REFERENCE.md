# API Reference Guide

Complete documentation of all REST API endpoints for the Disruption Management System.

## 📑 Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently, the API does not require authentication (development mode). For production, implement:
- API Key authentication
- JWT tokens
- OAuth 2.0

## Response Format

All responses are JSON with the following structure:

### Success Response (200, 201)
```json
{
  "status": "success",
  "data": {},
  "message": "Operation successful"
}
```

### Error Response (4xx, 5xx)
```json
{
  "status": "error",
  "error": "Error message",
  "code": 400
}
```

---

## Endpoints

### 1. GET /flights

**Description:** Retrieve all flights with disruption status

**Parameters:** None

**Response:**
```json
{
  "status": "success",
  "data": {
    "flights": [
      {
        "flight_id": "EY234",
        "airline": "Etihad Airways",
        "departure": "2024-01-15T08:00:00",
        "arrival": "2024-01-15T12:30:00",
        "origin": "DXB",
        "destination": "LHR",
        "status": "Delayed",
        "is_disrupted": true,
        "disruption_duration": 2.5,
        "total_passengers": 250,
        "aircraft_type": "Boeing 777-300ER"
      }
    ],
    "summary": {
      "total": 19,
      "disrupted_count": 7,
      "on_time_count": 12
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved flights
- `500 Internal Server Error` - Server error

---

### 2. GET /passengers

**Description:** Retrieve all disrupted passengers with optional filtering

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search by name/PNR | `search=John` |
| `tier` | string | Filter by tier | `tier=Gold` |
| `eligible` | boolean | Filter by eligibility | `eligible=true` |
| `limit` | number | Limit results | `limit=50` |
| `offset` | number | Pagination offset | `offset=0` |

**Example Request:**
```
GET /api/passengers?tier=Gold&eligible=true&limit=10
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "passengers": [
      {
        "passenger_id": "P001",
        "name": "John Doe",
        "pnr": "ABC123",
        "booking_reference": "ABC123XYZ",
        "email": "john@example.com",
        "phone": "+1-555-0100",
        "flight_id": "EY234",
        "ticket_price": 1200,
        "loyalty_status": "Gold Member",
        "seat_class": "Business",
        "tier": "Gold",
        "eligible": true,
        "booking_date": "2024-01-10T10:30:00",
        "has_connection": true
      }
    ],
    "summary": {
      "total": 150,
      "filtered_count": 40,
      "by_tier": {
        "Gold": 40,
        "Silver": 60,
        "Bronze": 50
      }
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved passengers
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Server error

---

### 3. GET /disruptions

**Description:** Retrieve all flight disruptions with affected passenger counts

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `type` | string | Filter by type | `type=Delayed` |
| `limit` | number | Limit results | `limit=10` |

**Example Request:**
```
GET /api/disruptions?type=Delayed&limit=10
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "disruptions": [
      {
        "disruption_id": "D001",
        "flight_id": "EY234",
        "airline": "Etihad Airways",
        "route": "DXB → LHR",
        "type": "Delayed",
        "duration_hours": 2.5,
        "reason": "Weather conditions at destination",
        "description": "Thunderstorm over London Heathrow",
        "affected_passengers": 250,
        "affected_by_tier": {
          "Gold": 40,
          "Silver": 60,
          "Bronze": 150
        },
        "created_at": "2024-01-15T08:45:00",
        "resolved_at": "2024-01-15T11:15:00"
      }
    ],
    "summary": {
      "total": 7,
      "by_type": {
        "Delayed": 4,
        "Cancelled": 2,
        "Diverted": 1
      },
      "total_affected": 1750
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved disruptions
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Server error

---

### 4. GET /recommendations

**Description:** Retrieve AI-generated passenger care recommendations

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `tier` | string | Filter by tier | `tier=Gold` |
| `passenger_id` | string | Get specific passenger | `passenger_id=P001` |
| `priority` | string | Filter by priority | `priority=high` |
| `limit` | number | Limit results | `limit=50` |

**Example Request:**
```
GET /api/recommendations?tier=Gold&limit=20
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "recommendations": [
      {
        "recommendation_id": "R001",
        "passenger_id": "P001",
        "passenger_name": "John Doe",
        "flight_id": "EY234",
        "tier": "Gold",
        "recommendation": "Rebook passenger on next available premium cabin flight with complimentary upgrade to first class. Provide hotel accommodation (5+ hour disruption), complimentary lounge access, and meal vouchers ($75). Offer travel insurance coverage.",
        "actions": [
          "premium_rebook",
          "upgrade_first_class",
          "hotel_accommodation",
          "lounge_access",
          "meal_vouchers_75",
          "travel_insurance"
        ],
        "priority": "high",
        "estimated_cost": 2500,
        "created_at": "2024-01-15T09:00:00",
        "ollama_model": "mistral"
      }
    ],
    "summary": {
      "total": 150,
      "by_tier": {
        "Gold": 40,
        "Silver": 60,
        "Bronze": 50
      },
      "by_priority": {
        "high": 40,
        "medium": 60,
        "low": 50
      },
      "estimated_total_cost": 257350
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved recommendations
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Server error

---

### 5. GET /manager-summary

**Description:** Retrieve KPI metrics for executive dashboard

**Parameters:** None

**Response:**
```json
{
  "status": "success",
  "data": {
    "kpis": {
      "total_disrupted_passengers": 150,
      "total_voucher_value": 257350,
      "vouchers_issued": 30,
      "passengers_reprotected": 40,
      "tier_distribution": {
        "Gold": 40,
        "Silver": 60,
        "Bronze": 50
      },
      "disruption_metrics": {
        "total_disruptions": 7,
        "avg_duration_hours": 2.3,
        "by_type": {
          "Delayed": 4,
          "Cancelled": 2,
          "Diverted": 1
        }
      },
      "recovery_metrics": {
        "avg_recovery_time_hours": 4.5,
        "passengers_requiring_hotel": 45,
        "passengers_with_connections": 60
      }
    },
    "trends": {
      "passenger_satisfaction": "82%",
      "compliance_rate": "95%",
      "cost_per_passenger": 1715.67
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved summary
- `500 Internal Server Error` - Server error

---

### 6. GET /health

**Description:** Health check endpoint for monitoring

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00",
  "uptime_seconds": 3600,
  "database_status": "connected",
  "ollama_status": "connected"
}
```

**Status Codes:**
- `200 OK` - Application is healthy
- `503 Service Unavailable` - Service is down

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "code": 400,
  "error": "Invalid query parameter: tier=Unknown"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": 404,
  "error": "Resource not found"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": 500,
  "error": "Internal server error",
  "message": "Database connection failed"
}
```

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Check query parameters |
| 401 | Unauthorized | Provide credentials |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Error | Contact support |

---

## Examples

### Example 1: Get All Flights

**Request:**
```bash
curl -X GET "http://localhost:5000/api/flights" \
  -H "Content-Type: application/json"
```

**Response (Success):**
```json
{
  "status": "success",
  "data": {
    "flights": [...],
    "summary": {
      "total": 19,
      "disrupted_count": 7
    }
  }
}
```

### Example 2: Search Passengers

**Request:**
```bash
curl -X GET "http://localhost:5000/api/passengers?search=John&tier=Gold" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "passengers": [...],
    "summary": {
      "total": 150,
      "filtered_count": 8
    }
  }
}
```

### Example 3: Get Gold Tier Recommendations

**Request:**
```bash
curl -X GET "http://localhost:5000/api/recommendations?tier=Gold&limit=10" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "recommendations": [...],
    "summary": {
      "total": 150,
      "by_tier": {
        "Gold": 40
      }
    }
  }
}
```

### Example 4: Get Manager Summary

**Request:**
```bash
curl -X GET "http://localhost:5000/api/manager-summary" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "kpis": {
      "total_disrupted_passengers": 150,
      "total_voucher_value": 257350,
      "vouchers_issued": 30,
      "passengers_reprotected": 40
    }
  }
}
```

---

## Rate Limiting

Currently no rate limiting. For production:
- Implement rate limiting (100 requests/minute per IP)
- Use API keys for quota management
- Monitor usage patterns

---

## Pagination

For large datasets, use pagination:

```bash
# Get results 0-50
GET /api/passengers?limit=50&offset=0

# Get results 50-100
GET /api/passengers?limit=50&offset=50
```

---

## Caching

API responses are not cached in development. For production:
- Implement Redis caching
- Set TTL based on data freshness requirements
- Use conditional requests (ETag, Last-Modified)

---

## CORS Configuration

Current CORS settings allow all origins. Update for production:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-15 | Initial API release |

---

**Last Updated:** January 12, 2026  
**API Status:** Production Ready
