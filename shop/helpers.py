import time
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
            start_time = time.perf_counter()
            func(*args, **kwargs)
            time_elapsed_ms = (time.perf_counter() - start_time) * 1000
            _print_sql_statements(print_mode, time_elapsed_ms)

        return wrapper

    return inner_decorator


def _print_sql_statements(print_mode, time_elapsed_ms):
    total_sql_time_ms = sum(map(lambda q: float(q["time"]), connection.queries)) * 1000
    print(
        f"\n{'-'*60}\n[{len(connection.queries)}] SQL statements executed "
        f"(Total time = {time_elapsed_ms:0.1f}ms, "
        f"SQL time = {total_sql_time_ms:0.1f}ms):\n"
    )
    for idx, query in enumerate(connection.queries, start=1):
        print(idx, _get_formatted_sql_statement(query["sql"], print_mode), "\n")
    print(f"\n{'-'*60}")


def _get_formatted_sql_statement(sql, print_mode):
    if print_mode == DebugTypes.SHORT:
        return sql[sql.find("FROM") :]
    return sql
