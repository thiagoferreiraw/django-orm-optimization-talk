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

## Running sample queries

In file `shop/samples.py`, we can find several good/bad examples of ORM queries. 

To run those queries, do:
```sh
$ poetry run python manage.py shell_plus
```

Then, in the python shell, run:
```python
# Using a "bad" example - this will run several unucessary queries
from shop.samples import list_orders_bad
list_orders_bad()
```
![sample-bad](https://user-images.githubusercontent.com/9268203/188282980-5ec2f999-41c6-4402-b2c1-dd15b4faf7e9.png)


Another example:

```python
# Using a "good" example - this is optimized
from shop.samples import list_orders_good
list_orders_good()
```

![sample-good](https://user-images.githubusercontent.com/9268203/188282977-161cf40f-f596-474c-ab41-2e5a6b7972f6.png)