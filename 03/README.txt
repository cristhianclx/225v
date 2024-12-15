# https://www.python.org/downloads/

# commands

# create and activate virtualenv

python -m venv .venv
.venv\Scripts\activate.bat

# activate virtualenv

.venv\Scripts\activate.bat

# install

pip install -r requirements.txt --upgrade

# utils

pip install flask
pip freeze

# flask

flask --app main run --reload

# database

flask --app main db init # init
flask --app main db migrate # create migration
flask --app main db upgrade # apply migration
flask --app main db downgrade # revert migration

# database

flask --app main shell

>>> from main import User, db
>>> user = User(first_name="cristhian", last_name="cueva", age=33, location="huancayo", country="PE")
>>> db.session.add(user)
>>> db.session.commit()

>>> from main import User, db
>>> User.query.all()