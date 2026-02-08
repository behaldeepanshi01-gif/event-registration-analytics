-- Event Registration & Attendance Analytics - SQL Queries
-- Author: Deepanshi Behal

-- ============================================================
-- 1. KPI SUMMARY BY EVENT
-- ============================================================
SELECT
    event_name,
    COUNT(*) AS total_registrations,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS attended,
    SUM(CASE WHEN attendance_status = 'No-Show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attendance_rate,
    ROUND(SUM(CASE WHEN attendance_status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS noshow_rate,
    ROUND(AVG(acquisition_cost), 2) AS avg_cost_per_reg
FROM event_registrations
GROUP BY event_name
ORDER BY total_registrations DESC;


-- ============================================================
-- 2. CHANNEL ATTRIBUTION - REGISTRATIONS & ATTENDANCE
-- ============================================================
SELECT
    channel_source,
    COUNT(*) AS registrations,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM event_registrations), 1) AS pct_of_total,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS attended,
    ROUND(SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attendance_rate,
    ROUND(AVG(acquisition_cost), 2) AS avg_cost_per_reg,
    ROUND(SUM(acquisition_cost) / SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END), 2) AS cost_per_attendee
FROM event_registrations
GROUP BY channel_source
ORDER BY registrations DESC;


-- ============================================================
-- 3. CHANNEL ROI RANKING (BEST TO WORST)
-- ============================================================
SELECT
    channel_source,
    ROUND(SUM(acquisition_cost) / SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END), 2) AS cost_per_attendee,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS total_attended,
    ROUND(SUM(acquisition_cost), 2) AS total_spend
FROM event_registrations
GROUP BY channel_source
ORDER BY cost_per_attendee ASC;


-- ============================================================
-- 4. CONVERSION FUNNEL
-- ============================================================
SELECT
    COUNT(*) AS registered,
    SUM(CASE WHEN attendance_status != 'Cancelled' THEN 1 ELSE 0 END) AS not_cancelled,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS attended,
    SUM(CASE WHEN attendance_status = 'Attended' AND engagement_score >= 6 THEN 1 ELSE 0 END) AS highly_engaged,
    SUM(CASE WHEN survey_completed = 'Yes' THEN 1 ELSE 0 END) AS survey_completed
FROM event_registrations;


-- ============================================================
-- 5. REGISTRATION TIMING VS ATTENDANCE
-- ============================================================
SELECT
    CASE
        WHEN julianday(event_date) - julianday(registration_date) <= 7 THEN '1-7 days before'
        WHEN julianday(event_date) - julianday(registration_date) <= 14 THEN '8-14 days before'
        WHEN julianday(event_date) - julianday(registration_date) <= 30 THEN '15-30 days before'
        ELSE '31-60 days before'
    END AS registration_window,
    COUNT(*) AS registrations,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS attended,
    ROUND(SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attendance_rate
FROM event_registrations
GROUP BY registration_window
ORDER BY attendance_rate DESC;


-- ============================================================
-- 6. TOP INDUSTRIES BY ATTENDANCE
-- ============================================================
SELECT
    industry,
    COUNT(*) AS registrations,
    SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) AS attended,
    ROUND(SUM(CASE WHEN attendance_status = 'Attended' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS attendance_rate
FROM event_registrations
GROUP BY industry
ORDER BY attended DESC;


-- ============================================================
-- 7. TOP JOB TITLES AMONG ATTENDEES
-- ============================================================
SELECT
    job_title,
    COUNT(*) AS attendees,
    ROUND(AVG(engagement_score), 1) AS avg_engagement
FROM event_registrations
WHERE attendance_status = 'Attended'
GROUP BY job_title
ORDER BY attendees DESC
LIMIT 10;
