from flask import (Blueprint, flash, g, json, redirect, request, render_template,
  session, url_for, jsonify)

from werkzeug.exceptions import abort

from daily_checklist.auth import login_required
from daily_checklist.db import get_db

bp = Blueprint('reports', __name__)

@bp.route('/report')
@login_required
def show_report():
  db = get_db()
  dates = db.execute(
    ' SELECT i.due_date, COUNT(*) count_all, SUM(CASE WHEN done==1 THEN 1 ELSE 0 end) count_done,  '
    ' (1.0 * SUM(CASE WHEN done==1 THEN 1 ELSE 0 end) / COUNT(*)) * 100 AS percentage '
    ' FROM item i JOIN user u ON i.user_id = u.id '
    ' GROUP BY due_date '
    ' ORDER BY due_date DESC'
    ).fetchall()
  return render_template('reports/list.html', dates = dates)

@bp.route('/chart_data')
@login_required
def apex_charts_data():
  db = get_db()
  data = db.execute(
    ' SELECT i.due_date, (1.0 * SUM(CASE WHEN done==1 THEN 1 ELSE 0 end) / COUNT(*)) * 100 percentage '
    ' FROM item i JOIN user u ON i.user_id = u.id GROUP BY due_date '
  ).fetchall()

  return jsonify(dict(data))