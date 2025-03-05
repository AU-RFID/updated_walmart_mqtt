#!/usr/bin/env python3
import os
import sys
import csv
import time
from datetime import datetime, timedelta, time as dtime
from pathlib import Path

import pytz  # for time zone conversions

# ------------------------------------------------------------------------------
# 1) CONFIG AND SETUP
# ------------------------------------------------------------------------------
# Adjust to your actual environment paths
base_dir = Path(os.getenv('WALMART_MQTT_BASE_DIR', Path.home()))
config_path = base_dir / 'walmart-MQTT-main' / 'config'

if not config_path.is_dir():
    raise FileNotFoundError(f"The config directory does not exist: {config_path}")

sys.path.insert(0, str(config_path))
import config  # import config.py

# InfluxDB parameters
db_url = config.DB_PARAMETER['db_url']
db_token = config.DB_PARAMETER['db_token']
db_org = config.DB_PARAMETER['db_org']
db_bucket = config.DB_PARAMETER['db_bucket']
db_measurement = config.DB_PARAMETER['db_measurement']

# If you haven't already: pip install influxdb-client
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url=db_url, token=db_token, org=db_org)
query_api = client.query_api()

# We assume local time is 6 hours behind UTC (e.g. America/Chicago)
LOCAL_TZ = pytz.timezone("America/Chicago")  # or "Etc/GMT+6" if you want to ignore DST.


# ------------------------------------------------------------------------------
# 2) HELPER: Convert local-naive datetime -> UTC datetime string
# ------------------------------------------------------------------------------
def local_to_utc_iso(local_naive_dt):
    """
    Takes a naive datetime (assumed local time = UTC-6) 
    and returns an ISO8601 string in UTC. e.g. "2025-01-24T12:00:00Z"
    """
    # Localize to the specified timezone (America/Chicago) and convert to UTC:
    localized = LOCAL_TZ.localize(local_naive_dt)
    utc_dt = localized.astimezone(pytz.utc)
    # Return an ISO8601 string with 'Z'
    return utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ')


# ------------------------------------------------------------------------------
# 3) DATA RETRIEVAL FUNCTION
# ------------------------------------------------------------------------------
def retrieve_and_save_data(start_local, stop_local, parent_folder):
    """
    Retrieves data for [start_local, stop_local) in local time (UTC-6),
    then queries InfluxDB in UTC, applying timeShift(-6h) to keep final results in local time.

    :param start_local: naive datetime (local time)
    :param stop_local: naive datetime (local time)
    :param parent_folder: where to save CSV
    """
    # Convert local naive datetimes into UTC ISO8601 for Influx
    start_str = local_to_utc_iso(start_local)
    stop_str = local_to_utc_iso(stop_local)

    # We'll name the file by the local 'stop' time
    file_timestamp = stop_local.strftime('%Y-%m-%d_%H-%M-%S')
    csv_filename = f"data_{file_timestamp}.csv"
    csv_file_path = os.path.join(parent_folder, csv_filename)

    # Build Flux query
    flux_query = f"""
    from(bucket: "{db_bucket}")
    |> range(start: time(v: "{start_str}"), stop: time(v: "{stop_str}"))
    |> filter(fn: (r) => r["_measurement"] == "{db_measurement}")
    |> timeShift(duration: -6h)  // <== SHIFT FROM UTC TO LOCAL
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> keep(columns: ["_time", "comp_id", "EPC", "antenna", "channel", "peakRSSI", "phase", "timestamp:eventNum"])
    |> drop(columns: ["result", "table"])
    """

    # Query Influx
    try:
        result = query_api.query(org=db_org, query=flux_query)
    except Exception as e:
        print(f"Error querying InfluxDB: {e}")
        return

    # Convert query results to a list of dicts for CSV
    csv_rows = []
    for table in result:
        for record in table.records:
            csv_rows.append(record.values)

    # If no data, define headers manually
    headers = csv_rows[0].keys() if csv_rows else [
        "_time", "comp_id", "EPC", "antenna", "channel", "peakRSSI", "phase", "timestamp:eventNum"
    ]

    # Write CSV
    os.makedirs(parent_folder, exist_ok=True)
    try:
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"   - Saved data chunk to {csv_file_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}")


def retrieve_15min_chunks_in_range(start_local, stop_local, data_folder):
    """
    Break [start_local, stop_local) (local time) into 15-min chunks
    and call retrieve_and_save_data() for each chunk.
    """
    if start_local >= stop_local:
        print("Start time must be earlier than stop time.")
        return

    os.makedirs(data_folder, exist_ok=True)

    chunk_start = start_local
    while chunk_start < stop_local:
        chunk_stop = chunk_start + timedelta(minutes=15)
        if chunk_stop > stop_local:
            chunk_stop = stop_local
        retrieve_and_save_data(chunk_start, chunk_stop, data_folder)
        chunk_start = chunk_stop


# ------------------------------------------------------------------------------
# 4) MODE 1: DAILY 2 AM
# ------------------------------------------------------------------------------
def mode_daily_2am():
    """
    Retrieve data from 2 AM yesterday to 2 AM today in local time (UTC-6),
    split into 15-minute chunks. 
    Then timeShift(-6h) in Flux keeps final times in local.
    """
    now_local = datetime.now()  # naive, but "current system time" in local environment
    today_2am_local = datetime.combine(now_local.date(), dtime(2, 0))  # 2 AM local naive

    # If we're before today's 2 AM, shift back one day
    if now_local < today_2am_local:
        today_2am_local -= timedelta(days=1)

    yesterday_2am_local = today_2am_local - timedelta(days=1)

    print(f"Retrieving from local {yesterday_2am_local} to {today_2am_local}")

    # folder named by date of "yesterday 2 AM"
    folder_timestamp = yesterday_2am_local.strftime('%Y-%m-%d')
    day_folder_name = f"data_{folder_timestamp}"
    day_folder_path = os.path.join(".", "data", day_folder_name)

    retrieve_15min_chunks_in_range(yesterday_2am_local, today_2am_local, day_folder_path)


# ------------------------------------------------------------------------------
# 5) MODE 2: CUSTOM DATE/TIME
# ------------------------------------------------------------------------------
def mode_custom_range():
    """
    Ask the user for a custom start/stop in local time
    (UTC-6). Then retrieve data in 15-min chunks, timeShift(-6h) in query.
    """
    print("\nEnter custom start time in local (UTC-6) using 'YYYY-MM-DD HH:MM:SS' format:")
    user_start = input("  e.g. 2025-01-24 06:00:00 => ")
    print("Enter custom stop time in local (UTC-6) using 'YYYY-MM-DD HH:MM:SS' format:")
    user_stop = input("  e.g. 2025-01-24 08:00:00 => ")

    try:
        start_dt = datetime.strptime(user_start, "%Y-%m-%d %H:%M:%S")
        stop_dt = datetime.strptime(user_stop, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date/time format. Please try again (YYYY-MM-DD HH:MM:SS).")
        return

    if start_dt >= stop_dt:
        print("Stop time must be after start time.")
        return

    folder_timestamp = start_dt.strftime('%Y-%m-%d_%H-%M-%S')
    custom_folder_name = f"custom_{folder_timestamp}"
    custom_folder_path = os.path.join(".", "data", custom_folder_name)

    print(f"\nRetrieving local time range {start_dt} to {stop_dt}")
    print(f"Saving 15-min increments into => {custom_folder_path}")

    retrieve_15min_chunks_in_range(start_dt, stop_dt, custom_folder_path)


# ------------------------------------------------------------------------------
# 6) MODE 3: REPEATED INTERVALS
# ------------------------------------------------------------------------------
def mode_repeated_intervals():
    """
    Original repeated retrieval approach (12 or 24 hours).
    - Immediately retrieve the last 1 hour offset by 30 minutes
    - Then in a loop:
       * Sleep for N hours (12 or 24)
       * Retrieve that entire chunk in 1-hour slices
    """
    print("Choose data retrieval interval (for repeated batches):")
    print("1. 12 hours")
    print("2. 24 hours")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        interval_hours = 12
        folder_prefix = "12hr"
    elif choice == "2":
        interval_hours = 24
        folder_prefix = "24hr"
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # 1) Immediate 1-hour retrieval offset by 30 minutes in local time
    now_local = datetime.now()
    init_stop_time = now_local - timedelta(minutes=30)
    init_start_time = init_stop_time - timedelta(hours=1)

    init_folder_timestamp = init_stop_time.strftime('%Y-%m-%d_%H-%M-%S')
    init_folder_name = f"IF_1hr_{init_folder_timestamp}"
    init_folder_path = os.path.join(".", "data", init_folder_name)
    os.makedirs(init_folder_path, exist_ok=True)

    print(f"\nPerforming initial 1-hour retrieval (local {init_start_time} to {init_stop_time})")
    retrieve_and_save_data(init_start_time, init_stop_time, init_folder_path)

    # 2) Continuous loop
    while True:
        print(f"\nSleeping for {interval_hours} hours...")
        time.sleep(interval_hours * 3600)

        now_local = datetime.now()
        big_window_stop = now_local - timedelta(minutes=30)
        big_window_start = big_window_stop - timedelta(hours=interval_hours)

        folder_timestamp = big_window_stop.strftime('%Y-%m-%d_%H-%M-%S')
        big_folder_name = f"{folder_prefix}_{folder_timestamp}"
        big_folder_path = os.path.join(".", "data", big_folder_name)
        os.makedirs(big_folder_path, exist_ok=True)

        print(f"\nRetrieving {interval_hours} x 1-hour files.")
        print(f"Overall local range: {big_window_start} to {big_window_stop}")
        print(f"Saving them in {big_folder_path}")

        slice_start = big_window_start
        for _ in range(interval_hours):
            slice_stop = slice_start + timedelta(hours=1)
            retrieve_and_save_data(slice_start, slice_stop, big_folder_path)
            slice_start = slice_stop

        print(f"\nDone storing {interval_hours} hour-chunks in {big_folder_name} folder.")


# ------------------------------------------------------------------------------
# 7) MAIN
# ------------------------------------------------------------------------------
def main():
    # If run with --auto, skip menu and do daily 2 AM
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print("Auto-mode (cron). Running daily 2 AM retrieval in local time (UTC-6).")
        mode_daily_2am()
        return

    # Show menu
    print("Choose an option:")
    print("1. Daily 2 AM range (yesterday 2 AM to today 2 AM, 15-min increments)")
    print("2. Custom date/time range (15-min increments, local time, with -6h shift in query)")
    print("3. Repeated intervals (original 12 or 24-hour approach)")
    user_choice = input("Enter your choice (1/2/3): ").strip()

    if user_choice == "1":
        mode_daily_2am()
    elif user_choice == "2":
        mode_custom_range()
    elif user_choice == "3":
        mode_repeated_intervals()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
