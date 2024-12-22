# https://www.python.org/downloads/

# commands

# create and activate virtualenv

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
