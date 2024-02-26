from datetime import datetime
from collections import defaultdict


MORNING_STARTING_HOUR = 6
AFTERNOON_STARTING_HOUR = 12
NIGHT_STARTING_HOUR = 18

ROUNDING_PRECISION = 2

class Entry:
    def __init__(self, average_temperature, probability_of_rain, date_time):
        self.average_temperature = average_temperature
        self.probability_of_rain = probability_of_rain
        self.date_time = date_time



def group_entries_by_day(data, grp_day):
    for e in data:
        entry = Entry(e["average_temperature"], e["probability_of_rain"], e["date_time"])
        entry_time = datetime.fromisoformat(entry.date_time.replace('Z', '+00:00'))
        key = entry_time.date()
        grp_day[key].append(entry)


def format_reader_friendly_date(day):
    return day.strftime("%A %B %d").replace(" 0", " ")


def process_each_day(entries) -> dict:
    morning_t, morning_r, afternoon_t, afternoon_r = [], [], [], []
    all_t = [entry.average_temperature for entry in entries]

    for e in entries:
        entry_time = datetime.fromisoformat(e.date_time.replace('Z', '+00:00'))
        # collect morning period entries
        if MORNING_STARTING_HOUR <= entry_time.hour < AFTERNOON_STARTING_HOUR:
            morning_t.append(e.average_temperature)
            morning_r.append(e.probability_of_rain)
        # collection afternoon period entries
        elif AFTERNOON_STARTING_HOUR <= entry_time.hour < NIGHT_STARTING_HOUR:
            afternoon_t.append(e.average_temperature)
            afternoon_r.append(e.probability_of_rain)

    summary = {
        # if no morning data, report insufficient data
        "morning_average_temperature": "Insufficient forecast data" if not morning_t else round(
            sum(morning_t) / len(morning_t)),
        "morning_chance_of_rain": "Insufficient forecast data" if not morning_r else round(
            sum(morning_r) / len(morning_r), ROUNDING_PRECISION),
        # if no afternoon data, report insufficient data
        "afternoon_average_temperature": "Insufficient forecast data" if not afternoon_t else round(
            sum(afternoon_t) / len(afternoon_t)),
        "afternoon_chance_of_rain": "Insufficient forecast data" if not afternoon_r else round(
            sum(afternoon_r) / len(afternoon_r), ROUNDING_PRECISION),
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

        day_name = format_reader_friendly_date(day)
        summaries[day_name] = summary

    return summaries
