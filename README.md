# bigMamma
Web app for visualizing sales and sport events data. 
It uses [Google sheer API](https://developers.google.com/sheets/api) and [All Sport DB API](https://allsportdb.com/Home/API).

Install
-------

Create a virtualenv and activate it :

    $ python3 -m venv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Or on Windows cmd :

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat
    $ pip install -r requirements.txt

Install bigMamma/sales :

    $ pip install -e .

Run
---

    $ export FLASK_APP=sales
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run
Open http://127.0.0.1:5000 in a browser. Use search bar to filter out data.

Test
----

    $ pip install '.[test]'
    $ pytest
