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