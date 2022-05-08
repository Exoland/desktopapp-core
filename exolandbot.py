#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from exoland import exoland, __version__
import exoland_bot
import sys

# Usage : exolandbot.py --help

_BOT_PERCENT_MARGIN = 1  # at least 1% benefit to exchange
_VERBOSE_MODE = False  # can be changed with --verbose parameter

_RETURN_CODE_BUY = 0
_RETURN_CODE_DO_NOT_BUY = 1
_RETURN_CODE_ERROR = 2


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
    '--historyfile', '-f',
    type=str,
    help='csv file with the exchange history',
    required=True,
)
@click.option(
    '--forceexchange',
    is_flag=True,
    help='force the exchange, ignoring the bot decision (you may lose money)',
)
@click.option(
    '--simulate', '-s',
    is_flag=True,
    help='do not really exchange your money if set',
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='verbose mode',
)
@click.version_option(
    version=__version__,
    message='%(prog)s, based on [exoland] package version %(version)s'
)
def main(device_id, token, simulate, historyfile, verbose, forceexchange):
    if token is None:
        print("You don't seem to have a exoland token")
        print("Please execute exoland_cli.py first to get one")
        sys.exit(_RETURN_CODE_ERROR)

    global _VERBOSE_MODE
    _VERBOSE_MODE = verbose
    rev = exoland(device_id=device_id, token=token)

    to_buy_or_not_to_buy(exoland=rev,
                         simulate=simulate,
                         filename=historyfile,
                         forceexchange=forceexchange)


def log(log_str=""):
    if _VERBOSE_MODE:
        print(log_str)


def to_buy_or_not_to_buy(exoland, simulate, filename, forceexchange):
    percent_margin = _BOT_PERCENT_MARGIN

    last_transactions = exoland_bot.get_last_transactions_from_csv(
                        filename=filename)
    last_tr = last_transactions[-1]  # The last transaction
    log()
    log("Last transaction : {}\n".format(last_tr))
    previous_currency = last_tr.from_amount.currency

    current_balance = last_tr.to_amount  # How much we currently have

    current_balance_in_other_currency = exoland.quote(
                                from_amount=current_balance,
                                to_currency=previous_currency)
    log("Today : {} in {} : {}\n".format(
        current_balance, previous_currency, current_balance_in_other_currency))

    last_sell = last_tr.from_amount  # How much did it cost before selling

    last_sell_plus_margin = exoland_bot.get_amount_with_margin(
                                    amount=last_sell,
                                    percent_margin=percent_margin)
    log("Min value to buy : {} + {}% (margin) = {}\n".format(
        last_sell,
        percent_margin,
        last_sell_plus_margin))

    buy_condition = current_balance_in_other_currency.real_amount > \
        last_sell_plus_margin.real_amount

    if buy_condition or forceexchange:
        if buy_condition:
            log("{} > {}".format(
                current_balance_in_other_currency,
                last_sell_plus_margin))
        elif forceexchange:
            log("/!\\ Force exchange option enabled")
        log("=> BUY")

        if simulate:
            log("(Simulation mode : do not really buy)")
        else:
            exchange_transaction = exoland.exchange(
                            from_amount=current_balance,
                            to_currency=previous_currency,
                            simulate=simulate)
            log("{} bought".format(exchange_transaction.to_amount.real_amount))
            log("Update history file : {}".format(filename))
            exoland_bot.update_historyfile(
                                    filename=filename,
                                    exchange_transaction=exchange_transaction)
        sys.exit(_RETURN_CODE_BUY)
    else:
        log("{} < {}".format(
            current_balance_in_other_currency,
            last_sell_plus_margin))
        log("=> DO NOT BUY")
        sys.exit(_RETURN_CODE_DO_NOT_BUY)


if __name__ == "__main__":
    main()
