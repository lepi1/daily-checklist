from flask import (Blueprint, flash, g, redirect, request, render_template,
  session, url_for)

from werkzeug.exceptions import abort

from daily_checklist.auth import login_required
from daily_checklist.db import get_db

bp = Blueprint('reports', __name__)

@bp.route('/report')
@login_required
def show_report():
  db = get_db()
  todos = db.execute(
    'SELECT i.id, status, note, due_date, done, user_id'
    ' FROM item i JOIN user u ON i.user_id = u.id ').fetchall()
    # TODO: group by due date
  return render_template('todo/index.html', todos = todos)