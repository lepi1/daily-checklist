# daily-checklist [WIP]

[![lepi1](https://circleci.com/gh/lepi1/daily-checklist.svg?style=svg)](https://circleci.com/gh/lepi1/daily-checklist/)

## A simple web application written in Python using the Flask framework. It uses a SQLite3 database.
You can enter tasks for a specific day into this application. These tasks can be marked as finished or unfinished. The success of these tasks can then be evaluated for individual days.

### Requirements:
**Python 3**
## Installation:

```
git clone git@github.com:lepi1/daily-checklist.git
```

```
cd daily-checklist
```

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python setup.py install
```

```
FLASK_APP=daily_checklist FLASK_ENV=development flask run
```