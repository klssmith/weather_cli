#!/usr/bin/env python
# coding=utf8

import argparse
import os
import sys

from pytz import timezone

from app.datapoint_client.client import DatapointClient


local_time = timezone("Europe/London")
parser = argparse.ArgumentParser()
parser.add_argument(
    "datatype", help="forecast or observations", choices=["forecast", "observations"]
)
parser.add_argument("site", help="the ID of the site that the data is for", type=int)


def run():
    check_api_key()

    args = parser.parse_args()

    client = DatapointClient(os.environ["DATAPOINT_API_KEY"])
    display_data(args.datatype, client, args.site)


def check_api_key():
    if not os.environ.get("DATAPOINT_API_KEY"):
        print("The DATAPOINT_API_KEY environment variable is not set.", file=sys.stderr)
        exit(1)


def display_data(data_type, client, site_id):
    if data_type == "forecast":
        data = client.get_3hourly_forecasts_for_site(site_id)
    elif data_type == "observations":
        data = client.get_obs_for_site(site_id)

    print_data(data)


def print_data(data):
    def format_datetime(dt):
        dt = dt.astimezone(local_time)
        return dt.strftime("%A %d %b %-I%p")

    for date, content in data.items():
        print(f" ⭐️\t{format_datetime(date)} \t⭐️ ")
        print("----------------------------------")

        for key, value in content.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    run()
