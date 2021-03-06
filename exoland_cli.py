#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from getpass import getpass
import uuid
import sys

from exoland import exoland, __version__, get_token_step1, get_token_step2, signin_biometric, extract_token

# Usage : exoland_cli.py --help

@click.command()
@click.option(
    '--device-id', '-d',
    envvar="exoland_DEVICE_ID",
    type=str,
    help='your exoland token (or set the env var exoland_DEVICE_ID)',
)
@click.option(
    '--token', '-t',
    envvar="exoland_TOKEN",
    type=str,
    help='your exoland token (or set the env var exoland_TOKEN)',
)
@click.option(
    '--language', '-l',
    type=str,
    help='language ("en" or "es"), for the csv header and separator',
    default='en'
)
@click.option(
    '--account', '-a',
    type=str,
    help='account name (ex : "EUR CURRENT") to get the balance for the account'
 )
@click.version_option(
    version=__version__,
    message='%(prog)s, based on [exoland] package version %(version)s'
)
def main(device_id, token, language, account):
    """ Get the account balances on exoland """
    
    if token is None:
        print("You don't seem to have a exoland token")
        answer = input("Would you like to generate a token [yes/no]? ")
        selection(answer)
        device_id = 'cli_{}'.format(uuid.getnode())  # Unique id for a machine
        while token is None:
            try:
                token = get_token(device_id=device_id)
            except Exception as e:
                login_error_handler(e)

    if device_id is None:
        device_id = 'exoland_cli'  # For retro-compatibility
    rev = exoland(device_id=device_id, token=token)
    account_balances = rev.get_account_balances()
    if account:
        print(account_balances.get_account_by_name(account).balance)
    else:
        print(account_balances.csv(lang=language))


def get_token(device_id):
    phone = input(
        "What is your mobile phone (used with your exoland "
        "account) [ex : +33612345678] ? ")
    password = getpass(
        "What is your exoland app password [ex: 1234] ? ")
    verification_channel = get_token_step1(
        device_id=device_id,
        phone=phone,
        password=password
    )

    if verification_channel.upper() == "EMAIL":
        print()
        print("Your verification code has been sent by email.")
        print("Take note of the link on the **Authenticate** button.")
        print("It should look like https://exoland.com/app/email-authenticate/<CODE>?scope=login")

    code = input(
        "Please enter the 6 digit code you received by {} "
        "[ex : 123456] : ".format(verification_channel)
    )

    response = get_token_step2(
        device_id=device_id,
        phone=phone,
        code=code,
    )

    if "thirdFactorAuthAccessToken" in response:
        access_token = response["thirdFactorAuthAccessToken"]
        print()
        print("Selfie 3rd factor authentication was requested.")
        selfie_filepath = input(
            "Provide a selfie image file path (800x600) [ex : selfie.png] ")
        response = signin_biometric(
            device_id, phone, access_token, selfie_filepath)

    token = extract_token(response)
    token_str = "Your token is {}".format(token)
    device_id_str = "Your device id is {}".format(device_id)

    dashes = len(token_str) * "-"
    print("\n".join(("", dashes, token_str, device_id_str, dashes, "")))
    print("You may use it with the --token of this command or set the "
          "environment variable in your ~/.bash_profile or ~/.bash_rc, "
          "for example :", end="\n\n")
    print(">>> exoland_cli.py --device-id={} --token={}".format(device_id, token))
    print("or")
    print('echo "export exoland_DEVICE_ID={}" >> ~/.bash_profile'
          .format(device_id))
    print('echo "export exoland_TOKEN={}" >> ~/.bash_profile'
          .format(token))
    return token

def selection(user_input):
    yes_list = ["yes", "ye", "ya", "y", "yeah"]
    no_list = ["no", "nah", "nope", "n"]

    user_input = user_input.lower()
    if user_input in yes_list:
        return
    elif user_input in no_list:
        print("Thanks for using the exoland desktop app!")
        sys.exit()
    else:
        print("Input not recognized, expecting 'yes' or 'no")
        sys.exit()

def login_error_handler(error):
    error_list = {
        "The string supplied did not seem to be a phone number" : \
            "Please check the supplied number and try again.",
        "Status code 401" : "Incorrect login details, please try again.",
        "phone is empty" : "You did not enter a phone number..."
    }
    error = str(error)
    for entry in error_list:
        if entry in error:
            print(error_list.get(entry))
            return
    print("An unknown error has occurred: {}".format(error))
    return

if __name__ == "__main__":
    main()
