import sys
import subprocess

import requests
import json
import datetime

import os

# Instructions in readme if you want your own api key to access latest data
PROPUBLICA_API_KEY = os.environ.get('PROPUBLICA_API_KEY')

# Loads the cached data if we have exceeded daily api requests
def cached_bills_data():
    try:
        with open("cached_data/bills.json", "r") as file:
            data = json.load(file)
            bills = data['bills']
            accessed_datetime = data['accessed_datetime']
            error_message = "HTTP Error\nUsing cached bills data from " + accessed_datetime
            
    except (FileNotFoundError, json.JSONDecodeError) as err:
        error_message = "HTTP Error\nNo cached data exists"
        bills = []

    return bills,error_message

def cached_subjects_data():
    try:
        with open("cached_data/subjects.json", "r") as file:
            data = json.load(file)
            subjects = data["subjects"]
            accessed_datetime = data['accessed_datetime']
            error_message = "HTTP Error\nUsing cached subjects data from " + accessed_datetime
            
    except (FileNotFoundError, json.JSONDecodeError) as err:
        error_message = "HTTP Error\nNo cached data exists"
        subjects = []
        
    return subjects,error_message

def subject_list():
    url = "https://api.propublica.org/congress/v1/bills/subjects.json"
    headers = {'X-API-Key': PROPUBLICA_API_KEY}
    error_message = ""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract the subject data from the response
        data = json.loads(response.text)
        subjects = data['results'][0]['subjects']

        cached_data = {
            "subjects": subjects,
            "accessed_datetime": str(datetime.datetime.now())
        }


        # Writes the cached data to a file in a folder
        if not os.path.exists("cached_data"):
            os.makedirs("cached_data")
        with open("cached_data/subjects.json", "w") as outfile:
            json.dump(cached_data, outfile)


    except requests.exceptions.HTTPError as err:
        #print(f"HTTP Error: {err}")
        subjects,error_message = cached_subjects_data()

    except requests.exceptions.RequestException as err:
        #print(f"Request Error: {err}")
        subjects,error_message = cached_subjects_data()


    return subjects,error_message

def bill_tracker(subject):

    # ProPublica API
    endpoint = "https://api.propublica.org/congress/v1/bills/search.json"

    # Headers for the API call
    headers = {"X-API-Key": PROPUBLICA_API_KEY}

    # Parameters for the API call
    params = {"query": subject}

    # A dictionary to keep track of number of bills introduced per day
    bills_counter = {}

    try:
        # API Call
        response = requests.get(endpoint, headers=headers, params=params)

        # Raise an exception if the status code isn't 200
        response.raise_for_status()

        # Extract the bill data from the response
        data = response.json()
        bills = data["results"][0]["bills"]
        
        cached_data = {
            "bills": bills,
            "accessed_datetime": str(datetime.datetime.now())
        }
        
        # Writes the cached data to a file in a new folder
        if not os.path.exists("cached_data"):
            os.makedirs("cached_data")
        with open("cached_data/bills.json", "w") as outfile:
            json.dump(cached_data, outfile) 

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        bills,error_message = cached_bills_data()
            
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        bills,error_message = cached_bills_data()

    return bills,error_message

