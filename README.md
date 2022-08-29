# django-orm-optimization-talk

## Installing
Make sure you have poetry installed, then run:
```
poetry install
poetry run python manage.py migrate
```

## Creating a sample database

```
poetry run python manage.py create_test_records
```

See available params with:
```
poetry run python manage.py create_test_records --help
```
