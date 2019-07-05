#!/usr/bin/env python3

import argparse
import sys

import logging


def run_cmd(args):
    print('here i go, running a cmd')
    import ipdb; ipdb.set_trace()


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
