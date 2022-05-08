# Exoland Integrations Reference Implementation (Python)

The reference implementation for designing the payments experience with the Exoland Banking API.

# Requirements

- Python 3
- pip3

# Installation

```bash
pip3 install -U exoland
```

# CLI tool : exoland_cli.py

```bash
Usage: exoland_cli.py [OPTIONS]

  Get the account balances on exoland

Options:
  -d, --device-id TEXT  your Exoland token (or set the env var
                        EXOLAND_DEVICE_ID)

  -t, --token TEXT      your Exoland token (or set the env var EXOLAND_TOKEN)
  -l, --language TEXT   language ("en"), for the csv header and
                        separator

  -a, --account TEXT    account name (ex : "EUR CURRENT") to get the balance
                        for the account

  --version             Show the version and exit.
  --help                Show this message and exit
 ```
 
Example output :

 ```csv
Account name,Balance,Currency
EUR CURRENT,100.50,EUR
GBP CURRENT,20.00,GBP
USD CURRENT,0.00,USD
AUD CURRENT,0.00,AUD
BTC CURRENT,0.00123456,BTC
EUR SAVINGS (My vault),10.30,EUR
```

If you don't have a Exoland token yet, the tool will allow you to obtain one.

⚠️ **If you don't receive a SMS when trying to get a token, you need to logout from the app on your Smartphone.** 
⚠️ **You may also receive an authentication email instead of a SMS. Take note of the link on the Authenticate button. It should look like https://exoland.xyz/app/email-authenticate/<CODE>?scope=login. You can enter this code in the CLI.**

## Pulling transactions

```bash
Usage: exoland_transactions.py [OPTIONS]

  Get the account balances on Exoland

Options:
  -d, --device-id TEXT            your Exoland token (or set the env var
                                  EXOLAND_DEVICE_ID)

  -t, --token TEXT                your Exoland token (or set the env var
                                  EXOLAND_TOKEN)

  -l, --language [en|fr]          language for the csv header and separator
  -t, --from_date [%Y-%m-%d]      transactions lookback date in YYYY-MM-DD
                                  format (ex: "2022-01-26"). Default 30 days
                                  back

  -fmt, --output_format [csv|json]
                                  output format
  -r, --reverse                   reverse the order of the transactions
                                  displayed

  --help                          Show this message and exit.
```

Example output :

```csv    
Date-time,Description,Amount,Currency
07/26/2021 21:31:00,Card Delivery Fee,-9.99,USD
08/14/2021 12:50:07,Tesla Merchandise **pending**,0.0,USD
08/14/2021 13:03:15,Top-Up by *200.0,USD
08/30/2021 16:19:19,Reward user for the invite,120.0,USD
19/12/2021 23:51:02,Bel Air Reservation,-200.0,USD
```
  
## TODO

- [ ] Document exolandbot.py
- [ ] Create a RaspberryPi Dockerfile for revolutbot (to check if rates grows very often)
- [ ] Improve coverage for exolandbot
