
import requests
import pandas as pd
import clickhouse_connect




url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 29.38385,
    "longitude": -94.90270,
    "start_date": "2026-09-01",
    "end_date": "2026-09-30",
    "hourly": "temperature_2m",
    "timezone": "America/Chicago",
    "timeformat": "unixtime"
}

response = requests.get(url, params=params, timeout=30)


data = response.json()

print("Weather data fetched successfully!")




hourly_df = pd.DataFrame(data["hourly"])


hourly_df["time"] = (
    pd.to_datetime(hourly_df["time"], unit="s", utc=True)
    .dt.tz_convert("America/Chicago")
)


hourly_df = hourly_df.rename(columns={
    "time": "observation_time",
    "temperature_2m": "temperature_c"
})


hourly_df["location"] = "Texas City"

# Arrange columns
hourly_df = hourly_df[
    ["location", "observation_time", "temperature_c"]
]

print("\nHourly DataFrame:")
print(hourly_df.head())

print("\nDataFrame shape:", hourly_df.shape)




client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="admin",
    password="admin123"
)

print("\nConnected to ClickHouse!")




# client.command("""
# CREATE DATABASE IF NOT EXISTS weather_db
# """)




# client.command("""
# CREATE TABLE IF NOT EXISTS weather_db.hourly_weather
# (
#     location String,
#     observation_time DateTime('America/Chicago'),
#     temperature_c Float64
# )
# ENGINE = MergeTree()
# ORDER BY (location, observation_time)
# """)

# print("Hourly table is ready!")




# client.command("""
# CREATE TABLE IF NOT EXISTS weather_db.daily_temperature
# (
#     location String,
#     weather_date Date,
#     min_temperature_c Float64,
#     max_temperature_c Float64
# )
# ENGINE = MergeTree()
# ORDER BY (location, weather_date)
# """)

# print("Daily table ")









# client.insert_df(
#     "weather_db.hourly_weather",
#     hourly_df
# )

# print("\nHourly data uploaded successfully!")




# client.command("""
# INSERT INTO weather_db.daily_temperature

# SELECT
#     location,

#     toDate(observation_time, 'America/Chicago') AS weather_date,

#     MIN(temperature_c) AS min_temperature_c,

#     MAX(temperature_c) AS max_temperature_c

# FROM weather_db.hourly_weather

# GROUP BY
#     location,
#     weather_date
# """)

# print("Daily minimum and maximum temperatures calculated!")



# hourly_count = client.query("""
# SELECT COUNT(*)
# FROM weather_db.hourly_weather
# """).result_rows[0][0]

# daily_count = client.query("""
# SELECT COUNT(*)
# FROM weather_db.daily_temperature
# """).result_rows[0][0]

# print("\n========== FINAL RESULTS ==========")

# print("Hourly records:", hourly_count)
# print("Daily records:", daily_count)

# print("\nDaily temperature summary:")

# result = client.query("""
# SELECT *
# FROM weather_db.daily_temperature
# ORDER BY weather_date
# LIMIT 10
# """)

# for row in result.result_rows:
#     print(row)

# print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")

# client.close()