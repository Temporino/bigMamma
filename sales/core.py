from flask import Blueprint, render_template
from sales.db import get_db
from sales import data

bp = Blueprint("core", __name__)


@bp.route('/')
def index():
    """render main index page for the app with loaded data"""
    db = get_db()

    # Get data from database
    sales = db.execute(
        'SELECT s.id, s.date, s.item_id, s.item_name, i.category, s.quantity, s.price, s.total_price, '
        'GROUP_CONCAT(e.name) AS events '
        ' FROM sales s JOIN items i ON s.item_id = i.id '
        ' LEFT JOIN events e ON s.date >= e.dateFrom AND s.date <= e.dateTo'
        ' GROUP BY s.id, s.date, s.item_id, s.item_name, i.category, s.quantity, s.price, s.total_price'
    ).fetchall()

    # pass data to the main index page
    return render_template('core/index.html', sales=sales)


@bp.route('/reload')
def reload():
    """reload input data on demand"""
    db = get_db()

    # todo test connection before deleting
    if data.test_connections():
        # delete existing data
        for table in ['sales', 'items', 'events']:
            db.execute(
                'DELETE FROM `{}`'.format(table)
            )
            db.execute(
                "UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = '{}'".format(table)
            )

        # load and populate new data
        data.load_all_data(db)

    return index()
