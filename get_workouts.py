#!/usr/bin/env python3

"""
Based on https://gist.github.com/niw/858c1ecaef89858893681e46db63db66

To obtain Bearer token, open dev tools,
login at https://www.nike.com/member/profile ,
and search for NIKE.COM in Network.  Save it to file shown below.
"""
import argparse
import datetime
import logging
import sys

import requests

ACTIVITIES_URL = 'https://api.nike.com/sport/v3/me/activities/after_time/{}'
ACTIVITY_URL = 'https://api.nike.com/sport/v3/me/activity/{}?metrics=ALL'
TOKEN_PATH = './bearer_token.txt'


def run_cmd(args):
    with open(TOKEN_PATH, 'r') as file:
        token = file.read().replace('\n', '')

    print(token)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    after_time = '1562284800000'
    url = ACTIVITIES_URL.format(after_time)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    for activity in response.json()['activities']:
        activity_id = activity['id']
        print(activity_id)
        url = ACTIVITY_URL.format(activity_id)
        response = requests.get(url, headers=headers).json()

        start_time = _ms_to_timestamp(response['start_epoch_ms'])
        duration = _ms_to_minutes_and_seconds(response['active_duration_ms'])

        print('start_time: {}'.format(start_time))
        print('duration: {}'.format(duration))


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
