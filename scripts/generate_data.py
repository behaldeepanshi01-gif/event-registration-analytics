"""
Generate simulated event registration dataset (2,000+ rows)
for Event Registration & Attendance Analytics project.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---- EVENT DEFINITIONS ----
events = {
    "Tech Summit 2024": {"type": "Flagship", "format": "In-Person", "count": 620, "base_date": "2024-03-15"},
    "Developer Conference 2024": {"type": "Flagship", "format": "In-Person", "count": 510, "base_date": "2024-06-10"},
    "AI Innovation Tour": {"type": "Regional", "format": "Hybrid", "count": 380, "base_date": "2024-09-05"},
    "Cloud Workshop Series": {"type": "Virtual", "format": "Virtual", "count": 310, "base_date": "2024-04-20"},
    "Industry Roadshow - East": {"type": "Regional", "format": "In-Person", "count": 190, "base_date": "2024-07-18"},
    "Industry Roadshow - West": {"type": "Regional", "format": "In-Person", "count": 170, "base_date": "2024-10-12"},
}

# ---- CHANNEL DEFINITIONS ----
# channel: (proportion of registrations, attendance rate)
channels = {
    "Email Campaign":  (0.32, 0.76),
    "LinkedIn Ad":     (0.20, 0.64),
    "Google Search":   (0.14, 0.71),
    "Direct/Website":  (0.13, 0.81),
    "Social Media":    (0.12, 0.56),
    "Referral":        (0.09, 0.86),
}

# ---- ATTENDEE ATTRIBUTES ----
job_titles = [
    "Data Analyst", "Marketing Manager", "IT Director", "Software Developer",
    "Product Manager", "Solutions Architect", "Business Analyst", "VP Marketing",
    "CTO", "Data Engineer", "Digital Marketing Specialist", "Program Manager"
]

industries = ["Technology", "Finance", "Healthcare", "Retail", "Education", "Manufacturing", "Media"]

company_sizes = ["1-50", "51-200", "201-1000", "1001-5000", "5000+"]

# ---- GENERATE DATA ----
rows = []
reg_id = 1

for event_name, event_info in events.items():
    n = event_info["count"]
    base_date = datetime.strptime(event_info["base_date"], "%Y-%m-%d")

    # registration window: 60 days before event to 2 days before
    for i in range(n):
        # pick channel based on proportions
        ch_names = list(channels.keys())
        ch_probs = [channels[c][0] for c in ch_names]
        ch_probs = [p / sum(ch_probs) for p in ch_probs]  # normalize
        channel = np.random.choice(ch_names, p=ch_probs)

        # registration date: 60 to 2 days before event
        days_before = np.random.randint(2, 61)
        reg_date = base_date - timedelta(days=int(days_before))

        # attendance based on channel + some noise
        base_attend_rate = channels[channel][1]
        # virtual events have higher no-show
        if event_info["format"] == "Virtual":
            base_attend_rate -= 0.10
        # late registrations have lower attendance
        if days_before < 7:
            base_attend_rate -= 0.08

        attended = np.random.random() < base_attend_rate

        # some people cancel (5% cancel rate)
        cancelled = np.random.random() < 0.05
        if cancelled:
            status = "Cancelled"
        elif attended:
            status = "Attended"
        else:
            status = "No-Show"

        # sessions
        if event_info["format"] == "Virtual":
            sessions_available = np.random.randint(3, 6)
        else:
            sessions_available = np.random.randint(5, 12)

        sessions_registered = np.random.randint(1, sessions_available + 1)

        if status == "Attended":
            sessions_attended = np.random.randint(1, sessions_registered + 1)
        else:
            sessions_attended = 0

        # engagement score (1-10)
        if status == "Attended":
            engagement = min(10, max(1, int(np.random.normal(6.5, 2))))
        elif status == "No-Show":
            engagement = min(3, max(1, int(np.random.normal(1.5, 0.8))))
        else:
            engagement = 0

        # post event survey
        if status == "Attended":
            survey_completed = "Yes" if np.random.random() < 0.45 else "No"
        else:
            survey_completed = "No"

        # cost per registration by channel
        cost_map = {
            "Email Campaign": round(np.random.uniform(2, 8), 2),
            "LinkedIn Ad": round(np.random.uniform(15, 45), 2),
            "Google Search": round(np.random.uniform(10, 35), 2),
            "Direct/Website": round(np.random.uniform(0, 2), 2),
            "Social Media": round(np.random.uniform(8, 25), 2),
            "Referral": round(np.random.uniform(0, 3), 2),
        }

        rows.append({
            "registration_id": reg_id,
            "event_name": event_name,
            "event_type": event_info["type"],
            "event_format": event_info["format"],
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "event_date": base_date.strftime("%Y-%m-%d"),
            "channel_source": channel,
            "job_title": np.random.choice(job_titles),
            "industry": np.random.choice(industries),
            "company_size": np.random.choice(company_sizes),
            "attendance_status": status,
            "sessions_registered": sessions_registered,
            "sessions_attended": sessions_attended,
            "engagement_score": engagement,
            "survey_completed": survey_completed,
            "acquisition_cost": cost_map[channel],
        })
        reg_id += 1

# ---- SAVE ----
df = pd.DataFrame(rows)
df.to_csv("C:/Users/Deepanshi/Desktop/event-registration-analytics/data/event_registrations.csv", index=False)
print(f"Dataset created: {len(df)} registrations")
print(f"\nEvents:\n{df['event_name'].value_counts()}")
print(f"\nAttendance Status:\n{df['attendance_status'].value_counts()}")
print(f"\nChannels:\n{df['channel_source'].value_counts()}")
