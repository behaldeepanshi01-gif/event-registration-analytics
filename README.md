# Event Registration & Attendance Analytics

> End-to-end funnel analysis of 2,180 event registrations — channel attribution, conversion optimization, and cost-per-attendee modeling across 6 marketing events.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)

## Business Context

Event marketers spend thousands per event but often lack clear visibility into which channels drive attendance, where registrants drop off, and what the true cost-per-attendee is. Built from experience managing 16+ corporate events at Hilton's Conrad Washington DC and 8 annual programs at Virginia Tech, this project demonstrates how event performance analytics can be done at scale.

## Dashboards

| | |
|:---:|:---:|
| ![Attendance Rate](dashboards/01_attendance_rate_by_event.png) | ![Channel Performance](dashboards/02_channel_performance.png) |
| **Attendance Rate by Event** | **Channel Performance** |
| ![Cost per Attendee](dashboards/03_cost_per_attendee.png) | ![Conversion Funnel](dashboards/04_conversion_funnel.png) |
| **Cost per Attendee by Channel** | **Registration-to-Attendance Funnel** |
| ![Registration Timing](dashboards/05_registration_timing.png) | ![Industry Breakdown](dashboards/06_attendees_by_industry.png) |
| **Registration Timing Impact** | **Attendees by Industry** |

## Key Findings

| Metric | Value | Insight |
|--------|-------|---------|
| Overall Attendance | **67.2%** | Across all 6 events |
| Best Channel | **Referral (80.2%)** | Highest attendance at $1.93/attendee |
| Most Expensive | **LinkedIn Ads ($49.26)** | Per attendee despite 60.8% attendance |
| Early Registration | **69.1% attendance** | 31-60 days out |
| Last-Minute Registration | **53.5% attendance** | 1-7 days out |

## Project Structure

```
event-registration-analytics/
├── data/
│   └── event_registrations.csv           # 2,180-row registration dataset
├── scripts/
│   ├── generate_data.py                  # Simulates event registration data
│   └── event_queries.sql                 # SQL queries for funnel and channel analysis
├── notebooks/
│   └── event_analysis.py                 # Full analysis with visualizations
├── dashboards/                           # 6 publication-ready visualizations
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

```bash
git clone https://github.com/behaldeepanshi01-gif/event-registration-analytics.git
cd event-registration-analytics
pip install -r requirements.txt
python scripts/generate_data.py
python notebooks/event_analysis.py
```

## Tools Used

- **Python**: pandas, numpy, matplotlib, seaborn, scipy.stats
- **SQL**: Event performance queries, channel attribution, funnel analysis
- **Power BI / Tableau**: Interactive dashboard creation

## Author

**Deepanshi Behal** | [LinkedIn](https://linkedin.com/in/bdeepanshi) | [GitHub](https://github.com/behaldeepanshi01-gif)
