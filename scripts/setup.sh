python3.8 -m pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
# python3 manage.py makemigrations snippify
# python3 manage.py migrate snippify
python3 manage.py migrate --run-syncdb