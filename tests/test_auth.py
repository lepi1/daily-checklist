import os
import tempfile

import pytest

import daily_checklist
from daily_checklist import db

@pytest.fixture
def client():
    app = daily_checklist.create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with daily_checklist.create_app().test_client() as client:
        with app.app_context():
            db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_not_logged_in(client):
    rv = client.get('/auth/login')
    assert b'Log In' in rv.data

def test_login_logout(client):
    """Make sure login and logout works."""
    app = daily_checklist.create_app()
    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data

