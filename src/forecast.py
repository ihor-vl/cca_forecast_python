from datetime import datetime
from collections import defaultdict

MORNING = "morning"
AFTERNOON = "afternoon"


MORNING_STARTING_HOUR = 6
AFTERNOON_STARTING_HOUR = 12
NIGHT_STARTING_HOUR = 18

ROUNDING_PRECISION = 2


class ForecastItem:
    def __init__(self, value, item_type, period):
        self.value = value
        self.type = item_type
        self.period: period


class Entry:
    def __init__(self, average_temperature, probability_of_rain, date_time):
        self.average_temperature = average_temperature
        self.probability_of_rain = probability_of_rain
        self.date_time = date_time

    def get_period(self):
        entry_time = datetime.fromisoformat(self.date_time.replace('Z', '+00:00'))
        if MORNING_STARTING_HOUR <= entry_time.hour < AFTERNOON_STARTING_HOUR:
            return MORNING
        elif AFTERNOON_STARTING_HOUR <= entry_time.hour < NIGHT_STARTING_HOUR:
            return AFTERNOON


class Summary:
    def __init__(self, forecast_items):
        self.forecast_items = forecast_items

    def get_morning_average_temperature(self):
        morning_temperature_items = [
            item for item in self.forecast_items
            if item.type == "temperature"
            and item.period == MORNING
        ]
        return sum(morning_temperature_items) / len(morning_temperature_items) if morning_temperature_items else None

    def get_afternoon_average_temperature(self):
        afternoon_temperature_items = [
            item for item in self.forecast_items
            if item.type == "temperature"
            and item.period == AFTERNOON
        ]
        return sum(afternoon_temperature_items) / len(afternoon_temperature_items) if afternoon_temperature_items \
            else None

    def get_morning_chance_of_rain(self):
        morning_chance_of_rain = [
            item for item in self.forecast_items
            if item.type == "rain"
            and item.period == MORNING
        ]
        return round(sum(morning_chance_of_rain) / len(morning_chance_of_rain), ROUNDING_PRECISION) if morning_chance_of_rain else None

    def get_afternoon_chance_of_rain(self):
        afternoon_chance_of_rain = [
            item for item in self.forecast_items
            if item.type == "rain"
            and item.period == AFTERNOON
        ]
        return round(sum(afternoon_chance_of_rain) / len(afternoon_chance_of_rain), ROUNDING_PRECISION) if afternoon_chance_of_rain else None

    def get_high_temperature(self):
        return max([item for item in self.forecast_items if item.type == "temperature"])

    def get_low_temperature(self):
        return min([item for item in self.forecast_items if item.type == "temperature"])


    def show(self) -> dict[str, str | float | None]:
        return {
            "morning_average_temperature": self.get_morning_average_temperature() or "Insufficient forecast data",
            "morning_chance_of_rain": self.get_morning_chance_of_rain() or "Insufficient forecast data",
            "afternoon_average_temperature": self.get_afternoon_average_temperature() or "Insufficient forecast data",
            "afternoon_chance_of_rain": self.get_afternoon_chance_of_rain() or "Insufficient forecast data",
            "high_temperature": self.get_high_temperature(),
            "low_temperature": self.get_low_temperature()
        }



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

    for entry in entries:
        if entry.get_period() == MORNING:
            morning_t.append(entry.average_temperature)
            morning_r.append(entry.probability_of_rain)
        elif entry.get_period() == AFTERNOON:
            afternoon_t.append(entry.average_temperature)
            afternoon_r.append(entry.probability_of_rain)

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
