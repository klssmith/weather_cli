#!/usr/bin/env python
# coding=utf8

import os
import pprint
import sys

from app.datapoint_client.client import DatapointClient


def run():
    check_api_key()
    check_args_are_valid()

    data_type, site = sys.argv[1], sys.argv[2]
    client = DatapointClient(os.environ["DATAPOINT_API_KEY"])

    if data_type == "forecast":
        display_forecast(client, site)
    elif data_type == "observations":
        display_observations(client, site)


def check_api_key():
    if not os.environ.get("DATAPOINT_API_KEY"):
        print("The DATAPOINT_API_KEY environment variable is not set.")


def check_args_are_valid():
    valid = False

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


def display_forecast(client, site_id):
    forecast = client.get_3hourly_forecasts_for_site(site_id)
    pprint.pprint(forecast)


def display_observations(client, site_id):
    observations = client.get_obs_for_site(site_id)
    pprint.pprint(observations)


if __name__ == "__main__":
    run()
