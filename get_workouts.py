#!/usr/bin/env python3

"""
Based on https://gist.github.com/niw/858c1ecaef89858893681e46db63db66

To obtain Bearer token, open dev tools,
login at https://www.nike.com/member/profile
and search for NIKE.COM in Network.  Save it to file shown below.

Graphs using Plotly https://plot.ly/python/bar-charts/#bar-chart-with-hover-text

Example usage:
./get_workouts.py

"""
import argparse
import datetime
import json
import logging
import os
import sys

import plotly.graph_objs as go
from plotly.offline import plot
import requests


ACTIVITIES_URL = 'https://api.nike.com/sport/v3/me/activities/after_time/{}'
ACTIVITY_URL = 'https://api.nike.com/sport/v3/me/activity/{}?metrics=ALL'
TOKEN_PATH = './bearer_token.txt'


def run_cmd(args):
    # First, Get every 'activity id' corresponding to a workout,
    # So we can later get each workout's activity info (start, duration)
    logger = logging.getLogger(__name__)
    with open(TOKEN_PATH, 'r') as file:
        token = file.read().replace('\n', '')

    headers = {'Authorization': 'Bearer {}'.format(token)}
    # TODO: hardcoded time, remove or make a passed in option
    # BUG: also, this seems it may only grab 2019 workouts due to start time
    after_time = '1562284800000'
    url = ACTIVITIES_URL.format(after_time)
    logger.info("GET {}".format(url))

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    activities = response.json()['activities']
    logger.debug("Found {} workouts".format(len(activities)))
    logger.debug("Going to GET each Workout Profile")
    os.makedirs(args.output_path, exist_ok=True)
    for activity in activities:
        activity_id = activity['id']
        logger.debug("GET {}".format(url))
        url = ACTIVITY_URL.format(activity_id)
        response = requests.get(url, headers=headers).json()

        start_time = _ms_to_timestamp(response['start_epoch_ms'])
        duration = _ms_to_minutes_and_seconds(response['active_duration_ms'])

        with open("{}/{}".format(args.output_path, activity_id), 'w+') as target:
            json.dump(response, target)

    logger.info("Saved workout data, Going to Generate Plot")
    generate_plotly_data(args)
    logger.info("Success, Open Your HTML File to See Results")


def generate_plotly_data(args):
    all_data_points = []

    for file_name in os.listdir(args.output_path):
        loaded_data = json.load(open(args.output_path + file_name))

        start_epoch = loaded_data['start_epoch_ms']
        duration_ms = loaded_data['active_duration_ms']

        all_data_points.append([start_epoch, duration_ms])

    # sort based on start date
    all_data_points.sort(key=lambda data_point: data_point[0])

    # get start times as readable timestamp
    all_start_times = [x[0] for x in all_data_points]
    all_start_times = [_ms_to_timestamp(x) for x in all_start_times]

    all_durations = [x[1] for x in all_data_points]
    all_durations = [_ms_to_minute(x) for x in all_durations]

    plot([go.Bar(x=all_start_times, y=all_durations)], filename='nike-workouts.html')


def _ms_to_minute(ms):
    seconds = ms / 1000

    return seconds / 60


def _ms_to_timestamp(ms):
    return datetime.datetime.fromtimestamp(ms / 1000).strftime('%B %d %Y, %I:%M:%S %p')


def _ms_to_minutes_and_seconds(ms):
    seconds = (ms / 1000) % 60
    seconds = int(seconds)
    minutes = (ms / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (ms / (1000 * 60 * 60)) % 24

    return ("%d hours, %d minutes, %d seconds" % (hours, minutes, seconds))


def create_argparser():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--output-path',
                           help='Path to Directory Output',
                           default='./workout_data/')

    argparser.set_defaults(func=run_cmd)

    return argparser


def main():
    argparser = create_argparser()
    args = argparser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.info('Starting script: {}'.format(__name__))
    logger.info('Command line arguments: {}'.format(args))

    args.func(args)


if __name__ == '__main__':
    sys.exit(main())
