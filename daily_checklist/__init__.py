import os

from flask_bootstrap import Bootstrap
from flask import Flask

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  bootstrap = Bootstrap(app)

  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'daily_checklist.sqlite')
  )

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # Hello page for testing
  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  # import db
  from . import db
  db.init_app(app)

  # import auth
  from . import auth
  app.register_blueprint(auth.bp)

  # import todos
  from . import todo
  app.register_blueprint(todo.bp)
  app.add_url_rule('/', endpoint='index')

  # import reports
  from . import reports
  app.register_blueprint(reports.bp)

  return app