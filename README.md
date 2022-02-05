# hntTax Email Service

This is a Python service that is periodically run to retrieve processed requests from our hnttax AWS database. 

The task retrieves new form entries from AWS postgres database, looks at the status, and prepares & sends an email to the user with the appropriate response. 


## Table of Contents
- [Initial Setup](#initial-setup)
  - [Environment variables](#environment-variables)
- [How to run](#how-to-run)
  - [Send CSV request emails](#send-csv-request-emails)


## Initial Setup

Before you can run the service, you need to clone this repo onto your machine:

```
git clone git@github.com:h-morgan/hnttax-emails.git
```

Next, `cd` into the project directory and either create (if first time) or activate the virtual environment. To __create__ the virtual environment for the first time, run (only need to do this once during setup):

```
python3 -m venv venv
```

To __activate__ it:
```
source venv/bin/activate
```

After activating the virtual environment, install the required Python packages:

```
pip3 install -r requirements.txt
```

### Environment variables

Create a `.env` file in the `src/` directory of this repository. The `.env` file needs to have the following environment variables populated for the service to run (connection details for the hntTax database, and a sender email username and password):

```
HNTTAX_DATABASE_HOST=host
HNTTAX_DATABASE_PORT=5432
HNTTAX_DATABASE_UN=username
HNTTAX_DATABASE_PW=password
HNTTAX_DATABASE_NAME=dbname

SENDER_UN=username
SENDER_PW=password
```

## How to Run

Right now, we only have support to send out emails for processed CSV requests. In the future, we'll have the ability to email out final Schedule C packages (a zipe file containing Schedule C pdf, txf, and any CSV's compiled.)

Navigate into the project's `src/` directory, where you will find `send.py`, which is the main entrypoint for the cli tool.

### Send CSV request emails

To send out emails for all recently processed CSV requests, run the following:

```
python send.py -r csv -s all
```
Where `-r` is the request type (csv, schc, or all) and `-s` is the status (processed, empty, error, etc.)

To send an email for a single row (ID) within the database, run:

```
python send.py -r csv --id 17
```
This will send the email for the row correspoding with ID #17 row in the csv table within the database.
