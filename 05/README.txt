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

# database

flask --app main shell

>>> from main import User, db
>>> user = User(first_name="cristhian", last_name="cueva", age=33, location="huancayo", country="PE")
>>> db.session.add(user)
>>> db.session.commit()

>>> from main import User, db
>>> User.query.all()

>>> from main import User, db
>>> User.query.get_or_404(1) # User.query.filter_by(id = 1).first()

>>> from main import User, db
>>> user = User.query.get_or_404(1)
>>> user.age = 34
>>> db.session.add(user)
>>> db.session.commit()

>>> from main import User, db
>>> user = User.query.get_or_404(2)
>>> db.session.delete(user)
>>> db.session.commit()

>>> from main import User, Message, db
>>> user = User.query.get_or_404(1)
>>> Message.query.filter_by(user = user).all()
>>> Message.query.filter_by(user_id = user_id).all()
