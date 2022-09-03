from functools import wraps

from django.db import connection, reset_queries


class DebugTypes:
    FULL = "full"
    SHORT = "short"


def debug_queries(print_mode=DebugTypes.SHORT):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            reset_queries()
            func(*args, **kwargs)
            _print_sql_statements(print_mode)

        return wrapper

    return inner_decorator


def _print_sql_statements(print_mode):
    print(f"\n{'-'*60}\nSQL statements:\n")
    for idx, query in enumerate(connection.queries, start=1):
        print(idx, _get_formatted_sql_statement(query["sql"], print_mode), "\n")
    print(f"\n{'-'*60}")


def _get_formatted_sql_statement(sql, print_mode):
    if print_mode == DebugTypes.SHORT:
        return sql[sql.find("FROM") :]
    return sql
