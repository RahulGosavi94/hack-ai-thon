#!/usr/bin/env python3
"""
Create GitHub issues with screenshots
Requires: pip install PyGithub
"""

import os
import base64
from github import Github, GithubException

# GitHub credentials - you'll need to set these as environment variables
# GITHUB_TOKEN should be set to your GitHub Personal Access Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "hack-ai-thon"
REPO_OWNER = "RahulGosavi94"

if not GITHUB_TOKEN:
    print("❌ Error: GITHUB_TOKEN environment variable not set")
    print("Please set your GitHub token:")
    print("  export GITHUB_TOKEN='your_token_here'")
    exit(1)

# Initialize GitHub API
try:
    github = Github(GITHUB_TOKEN)
    repo = github.get_user(REPO_OWNER).get_repo(REPO_NAME)
    print(f"✓ Connected to repository: {REPO_OWNER}/{REPO_NAME}")
except GithubException as e:
    print(f"❌ Error connecting to GitHub: {e}")
    exit(1)

# Screenshots and their descriptions
screenshots_data = [
    {
        "title": "📋 Flight List Tab",
        "file": "screenshots/flight_list.png",
        "description": """## Flight List Tab

This tab displays all flights with their current status:
- Flight number and details
- Departure and arrival information
- Current status (On-time/Delayed)
- Affected passengers count
- Quick action buttons

**Features:**
- View all flights in the system
- Identify disrupted flights at a glance
- Filter and sort capabilities
- Quick access to flight details
"""
    },
    {
        "title": "✈️ Flight Details Tab",
        "file": "screenshots/flight_details.png",
        "description": """## Flight Details Tab

Comprehensive view of individual flight details:
- Selected flight information
- Passenger manifest
- Disruption timeline
- Status history
- Recommendations panel

**Features:**
- Detailed flight information
- Passenger list with impact status
- Historical data and timeline
- Integration with recommendation engine
"""
    },
    {
        "title": "👥 Passenger Impact Tab",
        "file": "screenshots/passenger_impact.png",
        "description": """## Passenger Impact Tab

Shows all passengers affected by disruptions:
- Complete passenger list
- Impact status for each passenger
- Compensation eligibility
- Care requirements
- Individual passenger actions

**Features:**
- Search and filter passengers
- View passenger details
- Apply individual actions
- Track passenger care status
"""
    },
    {
        "title": "🤖 AI Suggestions Tab",
        "file": "screenshots/ai_suggestions.png",
        "description": """## AI Suggestions Tab

AI-powered recommendations for passenger care:
- Generated recommendations from Ollama LLM
- Hotel accommodation suggestions
- Meal voucher recommendations
- Rebooking options
- Cost impact analysis

**Features:**
- LLM-powered recommendations
- Automated suggestion generation
- Cost-benefit analysis
- Passenger-specific suggestions
"""
    },
    {
        "title": "📊 Manager Summary Tab",
        "file": "screenshots/manager_summary.png",
        "description": """## Manager Summary Tab

Executive dashboard with KPIs:
- Total passengers affected
- Cost impact
- Hotel rooms needed
- Meal vouchers issued
- Passengers reprotected
- Average cost per passenger

**Features:**
- Real-time KPI tracking
- Actual vs. recommended actions
- Mass action tracking
- Executive overview
"""
    },
    {
        "title": "🍽️ Mass Meal Issuance Tab",
        "file": "screenshots/mass_meal_issuance.png",
        "description": """## Mass Meal Issuance Tab

Bulk meal coupon distribution:
- Select multiple passengers
- Specify meal coupon amount
- Set quantity per passenger
- Apply to all selected passengers
- Track issued coupons

**Features:**
- Bulk passenger selection
- Batch meal coupon issuance
- Coupon value configuration
- Real-time processing
- Immediate KPI updates
"""
    },
    {
        "title": "✈️ Mass Rebooking Tab",
        "file": "screenshots/mass_rebooking.png",
        "description": """## Mass Rebooking Tab

Bulk passenger rebooking:
- Select multiple passengers
- Choose new flight
- View available flights
- Apply rebooking to selected passengers
- Track rebooking status

**Features:**
- Batch passenger selection
- Flight availability checking
- Bulk rebooking processing
- Rebooking confirmation
- Real-time KPI updates
"""
    },
]

# Create issues with screenshots
for shot_data in screenshots_data:
    try:
        title = shot_data["title"]
        file_path = shot_data["file"]
        description = shot_data["description"]
        
        # Read screenshot file
        if not os.path.exists(file_path):
            print(f"⚠️  Skipping {title}: file not found")
            continue
        
        # Prepare issue body with image reference
        issue_body = description + "\n\n### Screenshot\n"
        issue_body += f"![{title}]({file_path})\n"
        
        # Create the issue
        issue = repo.create_issue(
            title=title,
            body=issue_body,
            labels=["documentation", "screenshots", "UI"]
        )
        
        # Add screenshot as an asset
        print(f"✓ Created issue: {title}")
        print(f"  Issue #{issue.number}: {issue.html_url}")
        
    except GithubException as e:
        print(f"❌ Error creating issue for {title}: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✓ All issues created successfully!")
