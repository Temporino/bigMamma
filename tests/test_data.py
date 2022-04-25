from sales import data
from sales.db import get_db
import datetime


def test_connection_googlesheet():
    creds = data.connect_sheet_api()
    assert creds is not None


def test_connection_sportdb():
    params = {}
    response = data.request_constructor(params)
    assert response is not None
    assert response.status_code == 200


def test_load_sales_data(app):
    data_example = [['2021-02-01', 1, 'Pizza Mammargarita', 10, 10, 100]]
    loaded = False
    try:
        with app.app_context():
            db = get_db()
            data.load_datatable(db, data_example, 'sales')
            loaded = True
    except Exception as e:
        print(e)

    assert loaded


def test_load_events_data(app):
    data_example = [[{'name': 'Tour de France 2021', 'sport': 'Cycling', 'dateFrom': '2021-01-01',
                      'dateTo': '2021-01-31', 'location': [{'name': 'Europe'}]}]]
    loaded = False
    try:
        with app.app_context():
            db = get_db()
            data.load_datatable(db, data_example, 'events')
            loaded = True
    except Exception as e:
        print(e)

    assert loaded


def test_fetch_sport_events_data():
    sales_data_example = [[datetime.date.today().strftime('%Y-%m-%d'), None, None, None, None, None]]
    loaded = False
    try:
        responses = data.get_sport_events(sales_data_example)
        loaded = True
    except Exception as e:
        print(e)

    assert loaded


def test_should_not_fetch_events_without_sales_data():
    loaded = False
    try:
        responses = data.get_sport_events(None)
        if responses:
            loaded = True
    except Exception as e:
        print(e)

    assert not loaded
