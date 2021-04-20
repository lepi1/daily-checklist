from flask import (Blueprint, flash, g, redirect, request, render_template,
  session, url_for)

from werkzeug.exceptions import abort

from daily_checklist.auth import login_required
from daily_checklist.db import get_db
from datetime import datetime

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
  db = get_db()
  todos = db.execute(
    'SELECT i.id, note, due_date, done, user_id'
    ' FROM item i JOIN user u ON i.user_id = u.id ').fetchall()
  return render_template('todo/index.html', todos = todos)

@bp.route('/today')
@login_required
def show_today():
  db = get_db()
  todos = db.execute(
    ' SELECT i.id, note, due_date, done, user_id'
    ' FROM item i JOIN user u ON i.user_id = u.id '
    ' WHERE i.due_date IS (?)', (datetime.today().strftime('%Y-%m-%d'),)
  ).fetchall()
  return render_template('todo/today.html', todos = todos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    note = request.form['note']
    due_date = request.form['due_date']
    error = None

    if not note:
      error = 'Note is required.'

    if not due_date:
      error = 'Due date is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO item (note, due_date, user_id)'
        ' VALUES (?, ?, ?)', (note, due_date, g.user['id'])
      )
      db.commit()
      return redirect(url_for('todo.index'))

  return render_template('todo/create.html')

@bp.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
  db = get_db()
  db.execute('DELETE FROM item WHERE id = ?', (id, ))
  db.commit()
  return redirect(url_for('todo.index'))


@bp.route('/<int:id>/done', methods=('POST', ))
@login_required
def done(id):
  db = get_db()
  db.execute('UPDATE item SET done = ? WHERE id = ?', (1, id))
  db.commit()
  return redirect(url_for('todo.index'))

@bp.route('/<int:id>/undone', methods=('POST', ))
@login_required
def undone(id):
  db = get_db()
  db.execute('UPDATE item SET done = ? WHERE id = ?', (0, id))
  db.commit()
  return redirect(url_for('todo.index'))