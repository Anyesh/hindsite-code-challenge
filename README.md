# Hinsite Ind- Coding Challenge by Anish Shrestha

## Run the application locally

1. Create an .env file amd put it in the root dir

```
SECRET_KEY = ""
POSTGRES_DB=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
DB_HOST=""
DB_PORT=5432
```

2. Run the migrations

```
python manage.py makemigrations

python manage.py migrate
```

3. Run local server

```
python manage.py runserver
```
