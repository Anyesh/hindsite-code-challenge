# Hinsite Ind- Coding Challenge by Anish Shrestha

## Run the application locally

```
sudo make start
```

And that's all you have to do. You can check if app is running on `http://localhost`.

## Run manually

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
