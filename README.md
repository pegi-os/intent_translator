# intent_translator
This is for the Security Controller of I2NSF Framework

## Run
```bash
# Run venv
myenv\Scripts\activate # for Window
source ./myenv/bin/activate # for Mac

# Run Frontend
cd ./frontend
npm start

# Run Backend
cd ../backend
python manage.py runserver
```

## Backend Migration
```bash
cd ./backend
python manage.py makemigrations
python manage.py migrate
```
  

