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

![Screen Shot 2022-09-03 at 15 20 26](https://user-images.githubusercontent.com/9268203/188283454-683d145e-70f3-42e2-9f54-4f3ff20c7566.png)


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
<img width="787" alt="image" src="https://user-images.githubusercontent.com/9268203/189481719-c6c4cb3f-1b98-409b-8d6c-6acabd44f13a.png">



Another example:

```python
# Using a "good" example - this is optimized
from shop.samples import list_orders_good
list_orders_good()
```

<img width="839" alt="image" src="https://user-images.githubusercontent.com/9268203/189481726-94765ab5-5ae6-4242-97dc-68647d889d97.png">
