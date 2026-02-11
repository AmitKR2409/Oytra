# Member Cleanup Script

This project is a data cleaning script built in Python.

## Overview

The script processes a messy exported member file and produces:

- members_final.csv (cleaned CRM-ready file)
- quarantine.csv (low-quality or test data)

## Features

- Standardizes dates to YYYY-MM-DD format
- Removes duplicate users based on email
- Keeps most recent signup for multi-plan users
- Adds is_multi_plan flag
- Moves invalid/test data to quarantine file

## Tech Used

- Python
- Pandas

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Run the script:
   python main.py
