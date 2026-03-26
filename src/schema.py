"""
Database Schema Definition for SQL Agent

This module contains the database schema information that helps the agent
understand the structure of tables and generate accurate SQL queries.
"""

DATABASE_SCHEMA = """
DATABASE: Marketing Analytics Database

TABLE: marketing_data
Description: Contains daily marketing campaign performance metrics aggregated by region, location, channel, and site.

COLUMNS:
- date (DATE): The date when the marketing activity and reporting occurred
  * Format: YYYY-MM-DD
  * Use for: Daily trends, date range filtering, time-based analysis

- region (VARCHAR): The country where the lead was generated
  * Examples: 'US', 'CA', 'MMRI', etc.
  * Use for: Geographic analysis, regional performance comparison

- location_id (VARCHAR): Unique branch identifier used across the organization
  * Format: Branch/location code
  * Use for: Joining with other location-based data, unique location identification

- location_name (VARCHAR): Human-readable branch name
  * Examples: 'Sydney CBD', 'Melbourne North', etc.
  * Use for: Reporting, display purposes, location filtering

- campaign_type (VARCHAR): Marketing channel through which leads/appointments were generated
  * Examples: 'Paid Search', 'Social Media', 'Email', 'Display', 'Organic', etc.
  * Also referred to as: 'channel'
  * Use for: Channel performance analysis, attribution

- cmp_pgm (VARCHAR): Platform or site where the campaign ran
  * Examples: 'Google Ads', 'Facebook', 'Instagram', 'LinkedIn', etc.
  * Also referred to as: 'site', 'platform'
  * Use for: Platform performance comparison, budget allocation

- leads (INTEGER): Total number of leads generated
  * Aggregation level: Daily, by region, location_name, channel, and site
  * Use for: Lead volume analysis, conversion funnel top-of-funnel metrics

- appointments (INTEGER): Total number of appointments booked
  * Aggregation level: Daily, by region, location_name, channel, and site
  * Use for: Conversion analysis, appointment scheduling performance

- eoi (INTEGER): Total number of expressions of interest
  * Stands for: Expression of Interest
  * Aggregation level: Daily, by region, location_name, channel, and site
  * Use for: Interest level tracking, mid-funnel conversion metrics

- spend (FLOAT): Total marketing spend amount
  * Currency: Based on region
  * Aggregation level: Daily, by region, location_name, channel, and site
  * Use for: ROI calculation, budget tracking, cost per lead/appointment analysis

COMMON QUERIES:
- Daily performance: SELECT date, SUM(leads), SUM(appointments), SUM(spend) FROM marketing_data GROUP BY date
- Channel performance: SELECT campaign_type, SUM(leads), SUM(spend) FROM marketing_data GROUP BY campaign_type
- Regional analysis: SELECT region, location_name, SUM(leads) FROM marketing_data GROUP BY region, location_name
- ROI calculation: SELECT campaign_type, SUM(spend) / NULLIF(SUM(leads), 0) as cost_per_lead FROM marketing_data GROUP BY campaign_type

KEY METRICS:
- Cost per Lead (CPL): spend / leads
- Cost per Appointment (CPA): spend / appointments
- Lead to Appointment Rate: (appointments / leads) * 100
- EOI Rate: (eoi / leads) * 100
"""

def get_schema_description():
    """Returns the database schema description for the SQL agent"""
    return DATABASE_SCHEMA


# Alternative: Structured schema format for programmatic access
SCHEMA_DICT = {
    "marketing_data": {
        "description": "Daily marketing campaign performance metrics aggregated by region, location, channel, and site",
        "columns": {
            "date": {
                "type": "DATE",
                "nullable": False,
                "description": "Date when the marketing activity and reporting occurred"
            },
            "region": {
                "type": "VARCHAR",
                "nullable": True,
                "description": "Country where the lead was generated"
            },
            "location_id": {
                "type": "VARCHAR",
                "nullable": True,
                "description": "Unique branch identifier used across the organization"
            },
            "location_name": {
                "type": "VARCHAR",
                "nullable": True,
                "description": "Human-readable branch name across the organization"
            },
            "campaign_type": {
                "type": "VARCHAR",
                "nullable": True,
                "description": "Marketing channel through which leads/appointments were generated (also called 'channel')",
                "aliases": ["channel"]
            },
            "cmp_pgm": {
                "type": "VARCHAR",
                "nullable": True,
                "description": "Platform or site where the campaign ran",
                "aliases": ["site", "platform"]
            },
            "leads": {
                "type": "INTEGER",
                "nullable": True,
                "description": "Aggregated lead count for a day, region, location_name, channel & site level"
            },
            "appointments": {
                "type": "INTEGER",
                "nullable": True,
                "description": "Aggregated appointments count for a day, region, location_name, channel & site level"
            },
            "eoi": {
                "type": "INTEGER",
                "nullable": True,
                "description": "Aggregated expression of interest count for a day, region, location_name, channel & site level"
            },
            "spend": {
                "type": "FLOAT",
                "nullable": True,
                "description": "Marketing spend amount for a day, region, location_name, channel & site level"
            }
        },
        "primary_key": None,
        "indexes": ["date", "region", "campaign_type"]
    }
}
