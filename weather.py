#!/usr/bin/env python
# coding=utf8

import os
import sys

from pytz import timezone

from app.datapoint_client.client import DatapointClient


local_time = timezone("Europe/London")


def run():
    check_api_key()
    check_args_are_valid()

    data_type, site = sys.argv[1], sys.argv[2]
    client = DatapointClient(os.environ["DATAPOINT_API_KEY"])
    display_data(data_type, client, site)


def check_api_key():
    if not os.environ.get("DATAPOINT_API_KEY"):
        print("The DATAPOINT_API_KEY environment variable is not set.")
        exit()


def check_args_are_valid():
    if len(sys.argv) >= 3:
        valid = True

    if len(sys.argv) < 3:
        valid = False
    elif sys.argv[1] not in ("forecast", "observations"):
        valid = False
    else:
        try:
            int(sys.argv[2])
        except ValueError:
            valid = False

    if not valid:
        print_instructions()
        exit()


def print_instructions():
    print(
        """
        ⚠️ There was something wrong with the arguments you entered ️️️⚠️

        * The first argument must be <forecast> or <observations>
        * The second argument must be the ID of the site you want the data for
        """
    )


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
