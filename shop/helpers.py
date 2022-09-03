from functools import wraps

from django.db import connection, reset_queries


def debug_queries(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        func(*args, **kwargs)
        _print_sql_statements()

    return wrapper


def _print_sql_statements():
    print(f"\n{'-'*60}\nSQL statements:\n")
    for idx, query in enumerate(connection.queries, start=1):
        print(idx, _get_sql_statement_without_fields(query["sql"]), "\n")
    print(f"\n{'-'*60}")


def _get_sql_statement_without_fields(sql):
    return sql[sql.find("FROM") :]
