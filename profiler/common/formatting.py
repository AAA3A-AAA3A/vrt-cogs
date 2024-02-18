import math
import typing as t
from datetime import datetime, timedelta

from redbot.core.utils.chat_formatting import box
from tabulate import tabulate

from .models import DB, StatsProfile


def format_method_pages(method_key: str, data: t.List[StatsProfile]) -> t.List[str]:
    data = [i for i in data if i.func_profiles]
    pages = []
    for stats in data:
        ts = int(stats.timestamp.timestamp())
        exe_time = f"{stats.total_tt:.4f}s"
        if stats.total_tt < 1:
            exe_time = f"{stats.total_tt * 1000:.2f}ms"
        txt = (
            f"## {method_key}\n"
            f"- Execution time: {exe_time}\n"
            f"- Type: {stats.func_type.capitalize()}\n"
            f"- Is Coroutine: {stats.is_coro}\n"
            f"- Time Recorded: <t:{ts}:F> (<t:{ts}:R>)\n\n"
            f"Page {len(pages) + 1}/{len(data)}"
        )
        pages.append(txt)
    if not pages:
        pages.append("No data to display. Come back later.")
    return pages


def format_method_tables(data: t.List[StatsProfile]) -> t.List[str]:
    data = [i for i in data if i.func_profiles]
    tables = []
    for stats in data:
        table = format_func_profiles(stats)
        tables.append(table)
    return tables


def format_runtime_pages(
    db: DB,
    sort_by: str,
    query: str = None,
) -> t.List[str]:
    now = datetime.now()
    stats: t.Dict[str, list] = {}
    for methodlist in db.stats.values():
        for method_key, profiles in methodlist.items():
            if query and query not in method_key:
                continue
            if profiles[0].func_type == "command":
                method_key = f"{method_key} (C)"
            elif profiles[0].func_type == "listener":
                method_key = f"{method_key} (L)"
            elif profiles[0].func_type == "task":
                method_key = f"{method_key} (T)"
            max_runtime = max(profile.total_tt for profile in profiles)
            min_runtime = min(profile.total_tt for profile in profiles)
            avg_runtime = sum(profile.total_tt for profile in profiles) / len(profiles)

            # Calculate the calls per minute and total calls in the last specified delta
            calls_over_delta = [i for i in profiles if i.timestamp > (now - timedelta(hours=db.delta))]
            if not calls_over_delta:
                # Don't show any results beyond the set delta
                continue

            # Caclulate the min and max timestamp
            newest, oldest = (
                max(calls_over_delta, key=lambda i: i.timestamp),
                min(calls_over_delta, key=lambda i: i.timestamp),
            )
            timeframe_minutes = (newest.timestamp - oldest.timestamp).total_seconds() / 60
            # Now calculate the calls per minute
            calls_per_minute = len(calls_over_delta) / timeframe_minutes if timeframe_minutes else 0
            total_calls = len(calls_over_delta)
            stats[method_key] = [max_runtime, min_runtime, avg_runtime, calls_per_minute, total_calls]

    per_page = 10
    start = 0
    end = per_page
    page_count = math.ceil(len(stats) / per_page)
    delta_text = f"Last {'Hour' if db.delta == 1 else f'{db.delta}hrs'}"

    cols = ["Method", "Max", "Min", "Avg", "Calls/Min", delta_text]
    if sort_by == "Name":
        cols = ["[Method]", "Max", "Min", "Avg", "Calls/Min", delta_text]
        stats = dict(sorted(stats.items()))
    elif sort_by == "Max":
        cols = ["Method", "[Max]", "Min", "Avg", "Calls/Min", delta_text]
        stats = dict(sorted(stats.items(), key=lambda item: item[1][0], reverse=True))
    elif sort_by == "Min":
        cols = ["Method", "Max", "[Min]", "Avg", "Calls/Min", delta_text]
        stats = dict(sorted(stats.items(), key=lambda item: item[1][1], reverse=True))
    elif sort_by == "Avg":
        cols = ["Method", "Max", "Min", "[Avg]", "Calls/Min", delta_text]
        stats = dict(sorted(stats.items(), key=lambda item: item[1][2], reverse=True))
    elif sort_by == "CPM":
        cols = ["Method", "Max", "Min", "Avg", "[Calls/Min]", delta_text]
        stats = dict(sorted(stats.items(), key=lambda item: item[1][3], reverse=True))
    elif sort_by == "LHC":
        cols = ["Method", "Max", "Min", "Avg", "Calls/Min", f"[{delta_text}]"]
        stats = dict(sorted(stats.items(), key=lambda item: item[1][4], reverse=True))

    def _format(value: float):
        if value < 1:
            return f"{value * 1000:.1f}ms"
        return f"{value:.3f}s"

    pages = []
    for p in range(page_count):
        if end > len(stats):
            end = len(stats)

        rows = []
        for i in range(start, end):
            method_key = list(stats.keys())[i]
            max_runtime, min_runtime, avg_runtime, calls_per_minute, calls_last_hour = stats[method_key]

            rows.append(
                [
                    method_key,
                    _format(max_runtime),
                    _format(min_runtime),
                    _format(avg_runtime),
                    round(calls_per_minute, 4),
                    calls_last_hour,
                ]
            )
        page = (
            f"{box(tabulate(rows, headers=cols), lang='py')}\n"
            "(C) = Command\n"
            "(T) = Task Loop\n"
            "(L) = Listener\n"
            f"Page `{p + 1}/{page_count}`"
        )
        if query:
            page += f"\nCurrent Filter: `{query}`"

        pages.append(page)
        start += per_page
        end += per_page

    if not pages:
        pages.append("No data to display. Come back later.")
    return pages


def format_func_profiles(stats: StatsProfile):
    cols = [
        "Function",
        "ncalls",
        "tottime",
        "percall_tottime",
        "cumtime",
        "percall_cumtime",
        "file:line",
    ]
    rows = []
    for func, profile in stats.func_profiles.items():
        rows.append(
            [
                func,
                profile.ncalls,
                profile.tottime,
                profile.percall_tottime,
                profile.cumtime,
                profile.percall_cumtime,
                f"{profile.file_name}:{profile.line_number}",
            ]
        )
    return tabulate(rows, headers=cols)


def format_runtimes(stats: t.Dict[str, t.List[StatsProfile]]):
    rows = []
    for method_key, profiles in stats.items():
        for profile in profiles:
            if profile.total_tt < 1:
                exe_time = f"{profile.total_tt * 1000:.2f}ms"
            else:
                exe_time = f"{profile.total_tt:.4f}s"

            rows.append([method_key, exe_time, profile.is_command, profile.is_coro])
    cols = ["Method", "Time", "Command", "Coro"]
    return tabulate(rows, headers=cols)


def timedelta_format(delta: t.Optional[timedelta] = None, seconds: t.Optional[int] = None) -> str:
    try:
        obj = seconds if seconds is not None else delta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        ("Yr", 60 * 60 * 24 * 365),
        ("M", 60 * 60 * 24 * 30),
        ("d", 60 * 60 * 24),
        ("h", 60 * 60),
        ("m", 60),
        ("s", 1),
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            strings.append(f"{period_value}{period_name}")

    return ", ".join(strings)
