rm migrations/0*.py
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py migrate back_end
