# hntTax Email Service

This is a Python service that is periodically run to retrieve processed requests from our hnttax AWS database. 

The task retrieves new form entries from AWS postgres database, looks at the status, and prepares & sends an email to the user with the appropriate response. 


## Table of Contents
- [Initial Setup](#initial-setup)
- [How to run](#how-to-run)


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