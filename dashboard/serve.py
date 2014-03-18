from flask import Flask, request, jsonify, render_template
from dashboard.essearch import ESSearch
from dashboard.performance import estimate_missed_clicks
import datetime


app = Flask('search_performance_dashboard')


@app.route('/')
def front():
    return render_template('index.html')


def start_date():
    start_days_ago = request.args.get('start_days_ago', None)
    if start_days_ago is not None:
        start_days_ago = int(start_days_ago)
    else:
        start_days_ago = 14
    return datetime.date.today() - datetime.timedelta(days=start_days_ago)


def end_date():
    end_days_ago = request.args.get('end_days_ago', None)
    if end_days_ago is not None:
        end_days_ago = int(end_days_ago)
    else:
        end_days_ago = 0
    return datetime.date.today() - datetime.timedelta(days=end_days_ago)


def overall():
    es = ESSearch()
    return dict(
        stats=es.fetch_stats(start_date(), end_date())
    )


@app.route('/overall')
def overall_json():
    return jsonify(**overall())


def clicks():
    es = ESSearch()
    query = request.args.get('q', None)
    positions = es.click_positions(start_date(), end_date(), query=query)
    counts = [count for (pos, count) in positions]
    return dict(
        positions=positions,
        total=sum(counts),
        performance=estimate_missed_clicks(counts),
    )


@app.route('/clicks')
def click_positions_json():
    return jsonify(**clicks())
