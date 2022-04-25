from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import datetime, timedelta, date
from configparser import ConfigParser


#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

sheetapi = config_object["SHEETAPI"]
sportapi = config_object["SPORTAPI"]

# If modifying these scopes, delete the file token.json.
SCOPES = [sheetapi["SCOPE"]]

# The ID and range of the spreadsheet.
SALES_SPREADSHEET_ID = sheetapi["SALES_SPREADSHEET_ID"]
SALES_RANGE_NAME = sheetapi["SALES_RANGE_NAME"]
ITEMS_RANGE_NAME = sheetapi["ITEMS_RANGE_NAME"]

# All sport API credentials
AUTHORIZATION_KEY = sportapi["AUTHORIZATION_KEY"]
allsportdb = sportapi["URL"]


def connect_sheet_api():
    """
        Retrieve credentials for google sheet api.
        In case the credentials are not valid, try to refresh them.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("Token file found")
    else:
        print("no token found for google sheet api")

    if not creds:
        return
    # If there are no (valid) credentials available, request valid token
    if creds and creds.expired and creds.refresh_token:
        print("Credentials from token file has expired. Requesting new ones ...")
        creds.refresh(Request())

        # Save the credentials for the next run
        print("Saving new credentials to the token file ...")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def get_sales_data():
    """load sales data from the spreadsheet using Google Sheets API."""
    print("Getting credentials ...")
    creds = connect_sheet_api()

    print("Getting data from google sheet source ...")
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        sales = sheet.values().get(spreadsheetId=SALES_SPREADSHEET_ID,
                                    range=SALES_RANGE_NAME).execute()
        sales_values = sales.get('values', [])

        items = sheet.values().get(spreadsheetId=SALES_SPREADSHEET_ID,
                                   range=ITEMS_RANGE_NAME).execute()
        items_values = items.get('values', [])

        if not sales_values or not items_values:
            print('Data might be missing')

        return sales_values, items_values

    except HttpError as err:
        print(err)
        return [], []


def request_constructor(params):
    """build api request and handle timeout/retry errors"""
    url = allsportdb + '/calendar'
    retry_strategy = Retry(
        total=10,  # retry attempts
        status_forcelist=[429, 500, 502, 503, 504],  # server error to retry on
        backoff_factor=0.5  # exponential backoff factor to manage cooldown time
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    response = session.get(url, headers={'Authorization': 'Bearer {}'.format(AUTHORIZATION_KEY)},
                          params=params)
    return response


def get_sport_events(sales):
    """Retrieve sport events data from allsportdb api"""
    if not sales:
        return

    responses = []  # store api responses

    print("Getting sales data range ...")
    # Get sales data range (min date to max date)
    datefrom = datetime.strptime(min(sales, key=lambda x: x[0])[0], "%Y-%m-%d").date()
    dateto = datetime.strptime(max(sales, key=lambda x: x[0])[0], "%Y-%m-%d").date()

    # calculate the week number for min and max sale date
    # the week number is used as a parameter for api calls
    first_monday = (datefrom - timedelta(days=datefrom.weekday()))
    last_monday = (dateto - timedelta(days=dateto.weekday()))
    today = date.today() - timedelta(days=date.today().weekday())

    first_week = max(int((first_monday - today).days/7), -1)  # free api limited to last week
    last_week = max(int((last_monday - today).days/7), -1)  # free api limited to last week

    # loop through the week number range to cover all sales data
    for week in range(first_week, last_week+1):
        print("Requesting sport event data for the week {} ...".format(week))
        params = {'continent': 'Europe', 'week': week}  # retrieve european sport events and only the weeks concerned
        page = 1
        response = request_constructor(params)

        # increment searched pages if necessary
        while response.status_code == 200 and response.json():
            responses.append(response.json())
            page += 1
            params['page'] = page
            response = request_constructor(params)

    return responses


def load_datatable(db, data, table):
    """load one data input to a table in the database (db)"""

    if not data:
        print("no data to load for {}".format(table))
        return

    if table == "items":
        print("Loading data to items table ...")
        for row in data:
            db.execute(
                'INSERT INTO items (id, name, price, category)'
                ' VALUES (?, ?, ?, ?)',
                (row[0], row[1], row[2], row[3])
            )
            db.commit()

    elif table == "sales":
        print("Loading data to sales table ...")
        for row in data:
            db.execute(
                'INSERT INTO sales (date, item_id, quantity, item_name, price, total_price)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (row[0], row[1], row[2], row[3], row[4], row[5])
            )
            db.commit()

    elif table == "events":
        print("Loading data to events table ...")
        for row in data:
            if row:
                db.execute(
                    'INSERT INTO events (name, sport, dateFrom, dateTo, country)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (row[0]['name'], row[0]['sport'], row[0]['dateFrom'], row[0]['dateTo'], row[0]['location'][0]['name'])
                )
                db.commit()


def load_all_data(db):
    """load all input data to the created database"""

    if not db:
        return
    sales, items = get_sales_data()  # read sales data
    events = get_sport_events(sales)  # read sport event data

    # load data
    load_datatable(db, sales, 'sales')
    load_datatable(db, items, 'items')
    load_datatable(db, events, 'events')


def test_connections():
    """test connections to google sheet and all sport db APIs"""

    creds = connect_sheet_api()  # Google sheet
    service = build('sheets', 'v4', credentials=creds)
    response = request_constructor({'week': -2})  # Test request with no response

    return service and response.status_code == 200
