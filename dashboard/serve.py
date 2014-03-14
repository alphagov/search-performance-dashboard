from flask import Flask, request, jsonify, render_template
from dashboard.essearch import ESSearch
import datetime


app = Flask('search_performance_dashboard')


@app.route('/')
def front():
    return render_template('index.html')


def start_date():
    return datetime.date.today() - datetime.timedelta(days=7)


def end_date():
    return datetime.date.today() - datetime.timedelta(days=0)


def overall():
    es = ESSearch()
    return dict(
        stats=es.fetch_stats(start_date(), end_date())
    )


@app.route('/overall')
def overall_json():
    return jsonify(**overall())


def click_positions():
    es = ESSearch()
    query = request.args.get('q', None)
    return dict(
        positions=es.click_positions(start_date(), end_date(), query=query)
    )


@app.route('/click_positions')
def click_positions_json():
    return jsonify(**click_positions())
