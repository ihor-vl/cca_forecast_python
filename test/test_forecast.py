import unittest
from test.data import weather_data
from src.forecast import summarize_forecast


class ForecastTest(unittest.TestCase):
    def test_morning_average_temperature(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(10, summary["Sunday February 18"]["morning_average_temperature"])

    def test_morning_chance_of_rain(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(0.14, summary["Sunday February 18"]["morning_chance_of_rain"])

    def test_afternoon_average_temperature(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(16, summary["Sunday February 18"]["afternoon_average_temperature"])

    def test_afternoon_chance_of_rain(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(17, summary["Sunday February 18"]["high_temperature"])

    def test_high_temperature(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(0.4, summary["Sunday February 18"]["afternoon_chance_of_rain"])

    def test_low_temperature(self):
        summary = summarize_forecast(weather_data)
        self.assertEqual(6, summary["Sunday February 18"]["low_temperature"])

    def test_insufficient_morning_data(self):
        summary = summarize_forecast([
            {"date_time": "2024-02-18T00:00:00Z", "average_temperature": 12, "probability_of_rain": 0.35}
        ])
        self.assertEqual("Insufficient forecast data", summary["Sunday February 18"]["morning_average_temperature"])

    def test_insufficient_afternoon_data(self):
        summary = summarize_forecast([
            {"date_time": "2024-02-18T00:00:00Z", "average_temperature": 12, "probability_of_rain": 0.35}
        ])
        self.assertEqual("Insufficient forecast data", summary["Sunday February 18"]["afternoon_average_temperature"])

    def test_multiple_days(self):
        summary = summarize_forecast([
            {"date_time": "2024-02-18T00:00:00Z", "average_temperature": 12, "probability_of_rain": 0.35},
            {"date_time": "2024-02-19T00:00:00Z", "average_temperature": 12, "probability_of_rain": 0.35}
        ])
        self.assertEqual(2, len(summary))

    def test_no_entries(self):
        summary = summarize_forecast([])
        self.assertEqual(0, len(summary))


if __name__ == '__main__':
    unittest.main()
