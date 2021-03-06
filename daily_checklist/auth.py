import functools

from flask import (Blueprint, flash, g, redirect, request, render_template,
  session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from daily_checklist.db import get_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username:
      error = 'Username is required!'
    elif not password:
      error = 'Password is required!'
    elif db.execute(
      'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
      error = 'Already registered!'

    if error is None:
      db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
      )
      db.commit()
      return redirect(url_for('auth.login'))

    flash(error)

  return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
      'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
      error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))

    flash(error)

  return render_template('auth/login.html')

@bp.route('/edit-user', methods=('GET', 'POST'))
def edit_user():
  if request.method == 'POST':
    user_id = session['user_id']
    password = request.form['password']
    db = get_db()
    error = None

    if not password:
      error = 'Password is required!'

    if error is None:
      db.execute(
        'UPDATE user SET password = (?) WHERE id = (?)',
        (generate_password_hash(password), user_id)
      )
      db.commit()
      return redirect(url_for('todo.index'))

    flash(error)

  return render_template('auth/edit_user.html')

@bp.route('/delete-user', methods=['POST'])
def delete_user():
  user_id = session['user_id']
  db = get_db()

  db.execute(
    'DELETE FROM user WHERE id = (?)',
      (user_id, )
    )
  db.commit()
  session.clear()

  return redirect(url_for('auth.register'))

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)

  return wrapped_view