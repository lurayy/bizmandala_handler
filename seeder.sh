rm db.sqlite3
python3 manage.py makemigrations user_handler erp
python3 manage.py migrate
python3 manage.py shell < seeder.py