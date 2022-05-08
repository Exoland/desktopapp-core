#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os

from datetime import datetime
from datetime import timedelta

from exoland import exoland, __version__


@click.command()
@click.option(
    '--device-id', '-d',
    envvar="exoland_DEVICE_ID",
    type=str,
    help='your exoland token (or set the env var exoland_DEVICE_ID)',
    default='exoland_cli',
)
@click.option(
    '--token', '-t',
    envvar="exoland_TOKEN",
    type=str,
    help='your exoland token (or set the env var exoland_TOKEN)',
)
@click.option(
    '--language', '-l',
    type=click.Choice(['en', 'es']),
    help='language for the csv header and separator',
    default='en'
)
@click.option(
    '--from_date', '-t',
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help='transactions lookback date in YYYY-MM-DD format (ex: "2021-10-26"). Default 30 days back',
    default=(datetime.now()-timedelta(days=30)).strftime("%Y-%m-%d")
)
@click.option(
    '--output_format', '-fmt',
    type=click.Choice(['csv', 'json']),
    help="output format",
    default='csv',
)
@click.option(
    '--reverse', '-r',
    is_flag=True,
    help='reverse the order of the transactions displayed',
)
def main(device_id, token, language, from_date, output_format, reverse):
    """ Get the account balances on exoland """
    if token is None:
        print("You don't seem to have a exoland token. Use 'exoland_cli' to obtain one")
        exit(1)

    rev = exoland(device_id=device_id, token=token)
    account_transactions = rev.get_account_transactions(from_date)
    if output_format == 'csv':
        print(account_transactions.csv(lang=language, reverse=reverse))
    elif output_format == 'json':
        transactions = account_transactions.raw_list
        if reverse:
            transactions = reversed(transactions)
        print(json.dumps(transactions))
    else:
        print("output format {!r} not implemented".format(output_format))
        exit(1)


if __name__ == "__main__":
    main()
