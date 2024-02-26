pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --name admin --email admin@mail.com
xdg-open http://localhost:8000/admin/
python3 manage.py runserver localhost:8000