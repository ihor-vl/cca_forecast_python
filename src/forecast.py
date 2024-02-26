from datetime import datetime
from collections import defaultdict


def group_entries_by_day(data, grp_day):
    for e in data:
        entry_time = datetime.fromisoformat(e["date_time"].replace('Z', '+00:00'))
        key = entry_time.date()
        grp_day[key].append(e)


def process_each_day(entries) -> dict:
    morning_t, morning_r, afternoon_t, afternoon_r = [], [], [], []
    all_t = [entry["average_temperature"] for entry in entries]

    for e in entries:
        entry_time = datetime.fromisoformat(e["date_time"].replace('Z', '+00:00'))
        # collect morning period entries
        if 6 <= entry_time.hour < 12:
            morning_t.append(e["average_temperature"])
            morning_r.append(e["probability_of_rain"])
        # collection afternoon period entries
        elif 12 <= entry_time.hour < 18:
            afternoon_t.append(e["average_temperature"])
            afternoon_r.append(e["probability_of_rain"])

    summary = {
        # if no morning data, report insufficient data
        "morning_average_temperature": "Insufficient forecast data" if not morning_t else round(
            sum(morning_t) / len(morning_t)),
        "morning_chance_of_rain": "Insufficient forecast data" if not morning_r else round(
            sum(morning_r) / len(morning_r), 2),
        # if no afternoon data, report insufficient data
        "afternoon_average_temperature": "Insufficient forecast data" if not afternoon_t else round(
            sum(afternoon_t) / len(afternoon_t)),
        "afternoon_chance_of_rain": "Insufficient forecast data" if not afternoon_r else round(
            sum(afternoon_r) / len(afternoon_r), 2),
        "high_temperature": max(all_t),
        "low_temperature": min(all_t)
    }

    return summary


def summarize_forecast(data):
    grp_day = defaultdict(list)
    summaries = {}

    group_entries_by_day(data, grp_day)

    for day, entries in grp_day.items():
        summary = process_each_day(entries)

        # format reader-friendly date
        day_name = day.strftime("%A %B %d").replace(" 0", " ")
        summaries[day_name] = summary

    return summaries
