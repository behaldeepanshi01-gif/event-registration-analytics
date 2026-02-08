"""
Event Registration & Attendance Analytics
==========================================
Analysis of 2,180 event registrations across 6 marketing events.
Covers: KPI tracking, channel attribution, conversion funnel,
        attendance patterns, and engagement analysis.

Author: Deepanshi Behal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---- SETUP ----
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 150

output_dir = "C:/Users/Deepanshi/Desktop/event-registration-analytics/dashboards"
os.makedirs(output_dir, exist_ok=True)

# ---- LOAD DATA ----
df = pd.read_csv("C:/Users/Deepanshi/Desktop/event-registration-analytics/data/event_registrations.csv")
df["registration_date"] = pd.to_datetime(df["registration_date"])
df["event_date"] = pd.to_datetime(df["event_date"])
df["days_before_event"] = (df["event_date"] - df["registration_date"]).dt.days

print("=" * 60)
print("EVENT REGISTRATION & ATTENDANCE ANALYTICS")
print("=" * 60)
print(f"\nDataset: {len(df)} registrations across {df['event_name'].nunique()} events")
print(f"Date range: {df['registration_date'].min().date()} to {df['registration_date'].max().date()}")

# ============================================================
# 1. KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================
print("\n" + "=" * 60)
print("1. KEY PERFORMANCE INDICATORS")
print("=" * 60)

total_reg = len(df)
total_attended = len(df[df["attendance_status"] == "Attended"])
total_noshow = len(df[df["attendance_status"] == "No-Show"])
total_cancelled = len(df[df["attendance_status"] == "Cancelled"])

attendance_rate = total_attended / total_reg * 100
noshow_rate = total_noshow / total_reg * 100
cancel_rate = total_cancelled / total_reg * 100
avg_engagement = df[df["attendance_status"] == "Attended"]["engagement_score"].mean()
survey_rate = len(df[(df["survey_completed"] == "Yes")]) / total_attended * 100
avg_cost = df["acquisition_cost"].mean()
total_cost = df["acquisition_cost"].sum()
cost_per_attendee = total_cost / total_attended

print(f"\nTotal Registrations:     {total_reg:,}")
print(f"Total Attended:          {total_attended:,}")
print(f"Attendance Rate:         {attendance_rate:.1f}%")
print(f"No-Show Rate:            {noshow_rate:.1f}%")
print(f"Cancellation Rate:       {cancel_rate:.1f}%")
print(f"Avg Engagement Score:    {avg_engagement:.1f} / 10")
print(f"Survey Completion Rate:  {survey_rate:.1f}%")
print(f"Avg Cost per Reg:        ${avg_cost:.2f}")
print(f"Cost per Attendee:       ${cost_per_attendee:.2f}")

# ============================================================
# 2. EVENT PERFORMANCE COMPARISON
# ============================================================
print("\n" + "=" * 60)
print("2. EVENT PERFORMANCE COMPARISON")
print("=" * 60)

event_stats = df.groupby("event_name").agg(
    registrations=("registration_id", "count"),
    attended=("attendance_status", lambda x: (x == "Attended").sum()),
    no_shows=("attendance_status", lambda x: (x == "No-Show").sum()),
    avg_engagement=("engagement_score", lambda x: x[df.loc[x.index, "attendance_status"] == "Attended"].mean()),
    total_cost=("acquisition_cost", "sum"),
).reset_index()

event_stats["attendance_rate"] = (event_stats["attended"] / event_stats["registrations"] * 100).round(1)
event_stats["noshow_rate"] = (event_stats["no_shows"] / event_stats["registrations"] * 100).round(1)
event_stats["cost_per_attendee"] = (event_stats["total_cost"] / event_stats["attended"]).round(2)

print("\n" + event_stats[["event_name", "registrations", "attended", "attendance_rate", "noshow_rate", "cost_per_attendee"]].to_string(index=False))

# Chart: Attendance rate by event
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#2196F3" if r >= 65 else "#FF9800" for r in event_stats["attendance_rate"]]
bars = ax.barh(event_stats["event_name"], event_stats["attendance_rate"], color=colors, edgecolor="white")
ax.set_xlabel("Attendance Rate (%)")
ax.set_title("Attendance Rate by Event", fontsize=14, fontweight="bold")
for bar, val in zip(bars, event_stats["attendance_rate"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f"{val}%", va="center", fontsize=10)
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig(f"{output_dir}/01_attendance_rate_by_event.png", bbox_inches="tight")
plt.close()
print("\nSaved: 01_attendance_rate_by_event.png")

# ============================================================
# 3. CHANNEL ATTRIBUTION ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("3. CHANNEL ATTRIBUTION ANALYSIS")
print("=" * 60)

channel_stats = df.groupby("channel_source").agg(
    registrations=("registration_id", "count"),
    attended=("attendance_status", lambda x: (x == "Attended").sum()),
    avg_cost=("acquisition_cost", "mean"),
    total_cost=("acquisition_cost", "sum"),
    avg_engagement=("engagement_score", lambda x: x[df.loc[x.index, "attendance_status"] == "Attended"].mean()),
).reset_index()

channel_stats["attendance_rate"] = (channel_stats["attended"] / channel_stats["registrations"] * 100).round(1)
channel_stats["cost_per_attendee"] = (channel_stats["total_cost"] / channel_stats["attended"]).round(2)
channel_stats["reg_share"] = (channel_stats["registrations"] / total_reg * 100).round(1)
channel_stats = channel_stats.sort_values("registrations", ascending=False)

print("\n" + channel_stats[["channel_source", "registrations", "reg_share", "attendance_rate", "avg_cost", "cost_per_attendee"]].to_string(index=False))

# Chart: Channel performance - registrations vs attendance rate
fig, ax1 = plt.subplots(figsize=(10, 5))
x = range(len(channel_stats))
bars = ax1.bar(x, channel_stats["registrations"], color="#2196F3", alpha=0.8, label="Registrations")
ax1.set_ylabel("Registrations", color="#2196F3")
ax1.set_xticks(x)
ax1.set_xticklabels(channel_stats["channel_source"], rotation=25, ha="right")

ax2 = ax1.twinx()
ax2.plot(x, channel_stats["attendance_rate"], color="#FF5722", marker="o", linewidth=2, label="Attendance Rate")
ax2.set_ylabel("Attendance Rate (%)", color="#FF5722")
ax2.set_ylim(0, 100)

ax1.set_title("Channel Performance: Volume vs Quality", fontsize=14, fontweight="bold")
fig.legend(loc="upper right", bbox_to_anchor=(0.95, 0.95))
plt.tight_layout()
plt.savefig(f"{output_dir}/02_channel_performance.png", bbox_inches="tight")
plt.close()
print("\nSaved: 02_channel_performance.png")

# Chart: Cost per attendee by channel
fig, ax = plt.subplots(figsize=(10, 5))
ch_sorted = channel_stats.sort_values("cost_per_attendee", ascending=True)
colors = ["#4CAF50" if c < 15 else "#FF9800" if c < 30 else "#F44336" for c in ch_sorted["cost_per_attendee"]]
bars = ax.barh(ch_sorted["channel_source"], ch_sorted["cost_per_attendee"], color=colors, edgecolor="white")
ax.set_xlabel("Cost per Attendee ($)")
ax.set_title("Cost per Attendee by Channel (Lower = Better ROI)", fontsize=14, fontweight="bold")
for bar, val in zip(bars, ch_sorted["cost_per_attendee"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, f"${val:.2f}", va="center", fontsize=10)
plt.tight_layout()
plt.savefig(f"{output_dir}/03_cost_per_attendee.png", bbox_inches="tight")
plt.close()
print("Saved: 03_cost_per_attendee.png")

# ============================================================
# 4. CONVERSION FUNNEL
# ============================================================
print("\n" + "=" * 60)
print("4. CONVERSION FUNNEL")
print("=" * 60)

funnel_stages = ["Registered", "Not Cancelled", "Attended", "Engaged (Score 6+)", "Survey Completed"]
funnel_values = [
    total_reg,
    total_reg - total_cancelled,
    total_attended,
    len(df[(df["attendance_status"] == "Attended") & (df["engagement_score"] >= 6)]),
    len(df[df["survey_completed"] == "Yes"]),
]

print(f"\n{'Stage':<30} {'Count':>8} {'Rate':>10}")
print("-" * 50)
for stage, val in zip(funnel_stages, funnel_values):
    rate = val / total_reg * 100
    print(f"{stage:<30} {val:>8,} {rate:>9.1f}%")

# Chart: Funnel
fig, ax = plt.subplots(figsize=(10, 5))
colors_funnel = ["#2196F3", "#42A5F5", "#66BB6A", "#FFA726", "#EF5350"]
bars = ax.barh(funnel_stages[::-1], [v/total_reg*100 for v in funnel_values[::-1]],
               color=colors_funnel[::-1], edgecolor="white", height=0.6)
ax.set_xlabel("% of Total Registrations")
ax.set_title("Registration-to-Engagement Conversion Funnel", fontsize=14, fontweight="bold")
for bar, val in zip(bars, funnel_values[::-1]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val:,} ({val/total_reg*100:.1f}%)", va="center", fontsize=10)
ax.set_xlim(0, 110)
plt.tight_layout()
plt.savefig(f"{output_dir}/04_conversion_funnel.png", bbox_inches="tight")
plt.close()
print("\nSaved: 04_conversion_funnel.png")

# ============================================================
# 5. REGISTRATION TIMING TRENDS
# ============================================================
print("\n" + "=" * 60)
print("5. REGISTRATION TIMING ANALYSIS")
print("=" * 60)

# Attendance rate by days before event
timing_bins = pd.cut(df["days_before_event"], bins=[0, 7, 14, 30, 60], labels=["1-7 days", "8-14 days", "15-30 days", "31-60 days"])
timing_stats = df.groupby(timing_bins, observed=True).agg(
    registrations=("registration_id", "count"),
    attended=("attendance_status", lambda x: (x == "Attended").sum()),
).reset_index()
timing_stats.columns = ["timing_window", "registrations", "attended"]
timing_stats["attendance_rate"] = (timing_stats["attended"] / timing_stats["registrations"] * 100).round(1)

print(f"\n{'Registration Window':<20} {'Registrations':>15} {'Attendance Rate':>18}")
print("-" * 55)
for _, row in timing_stats.iterrows():
    print(f"{row['timing_window']:<20} {row['registrations']:>15,} {row['attendance_rate']:>17.1f}%")

# Chart
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(timing_stats["timing_window"].astype(str), timing_stats["attendance_rate"],
       color=["#F44336", "#FF9800", "#4CAF50", "#2196F3"], edgecolor="white")
ax.set_ylabel("Attendance Rate (%)")
ax.set_xlabel("Registration Window (Days Before Event)")
ax.set_title("Earlier Registrations = Higher Attendance", fontsize=14, fontweight="bold")
ax.set_ylim(0, 100)
for i, val in enumerate(timing_stats["attendance_rate"]):
    ax.text(i, val + 1.5, f"{val}%", ha="center", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/05_registration_timing.png", bbox_inches="tight")
plt.close()
print("\nSaved: 05_registration_timing.png")

# ============================================================
# 6. ATTENDEE DEMOGRAPHICS
# ============================================================
print("\n" + "=" * 60)
print("6. ATTENDEE DEMOGRAPHICS")
print("=" * 60)

# Top job titles by attendance
job_stats = df[df["attendance_status"] == "Attended"].groupby("job_title").agg(
    count=("registration_id", "count"),
    avg_engagement=("engagement_score", "mean"),
).sort_values("count", ascending=False).head(8)

print("\nTop Job Titles (Attended):")
print(job_stats.round(1).to_string())

# Industry breakdown
ind_stats = df.groupby("industry").agg(
    registrations=("registration_id", "count"),
    attended=("attendance_status", lambda x: (x == "Attended").sum()),
).reset_index()
ind_stats["attendance_rate"] = (ind_stats["attended"] / ind_stats["registrations"] * 100).round(1)
ind_stats = ind_stats.sort_values("attended", ascending=False)

print(f"\n{'Industry':<20} {'Registrations':>15} {'Attended':>10} {'Rate':>10}")
print("-" * 55)
for _, row in ind_stats.iterrows():
    print(f"{row['industry']:<20} {row['registrations']:>15} {row['attended']:>10} {row['attendance_rate']:>9.1f}%")

# Chart: Industry breakdown
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(ind_stats["industry"], ind_stats["attended"], color="#2196F3", edgecolor="white")
ax.set_ylabel("Attendees")
ax.set_title("Attendees by Industry", fontsize=14, fontweight="bold")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(f"{output_dir}/06_attendees_by_industry.png", bbox_inches="tight")
plt.close()
print("\nSaved: 06_attendees_by_industry.png")

# ============================================================
# 7. KEY FINDINGS SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("7. KEY FINDINGS & RECOMMENDATIONS")
print("=" * 60)

best_channel = channel_stats.loc[channel_stats["cost_per_attendee"].idxmin()]
worst_channel = channel_stats.loc[channel_stats["cost_per_attendee"].idxmax()]
best_event = event_stats.loc[event_stats["attendance_rate"].idxmax()]

print(f"""
FINDINGS:
1. Overall attendance rate is {attendance_rate:.1f}% with a {noshow_rate:.1f}% no-show rate
2. Best ROI channel: {best_channel['channel_source']} (${best_channel['cost_per_attendee']:.2f}/attendee)
3. Most expensive channel: {worst_channel['channel_source']} (${worst_channel['cost_per_attendee']:.2f}/attendee)
4. Highest attendance event: {best_event['event_name']} ({best_event['attendance_rate']}%)
5. Early registrants (31-60 days out) have significantly higher attendance rates
6. Only {survey_rate:.1f}% of attendees completed post-event surveys

RECOMMENDATIONS:
1. Increase budget allocation to {best_channel['channel_source']} and Referral channels - highest ROI
2. Reduce spend on {worst_channel['channel_source']} or improve targeting to increase conversion
3. Send reminder campaigns to registrants in the final 7 days to reduce no-shows
4. Incentivize post-event survey completion to improve the {survey_rate:.1f}% response rate
5. Focus early-bird promotions 30+ days before events to lock in higher attendance
""")

print("=" * 60)
print("Analysis complete. All charts saved to /dashboards folder.")
print("=" * 60)
