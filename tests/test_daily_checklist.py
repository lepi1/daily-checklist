import os
import tempfile

import pytest

from daily_checklist import daily_checklist


@pytest.fixture
def client():
    db_fd, daily_checklist.app.config['DATABASE'] = tempfile.mkstemp()
    daily_checklist.app.config['TESTING'] = True

    with daily_checklist.app.test_client() as client:
        with daily_checklist.app.app_context():
            daily_checklist.init_db()
        yield client

    os.close(db_fd)
    os.unlink(daily_checklist.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data