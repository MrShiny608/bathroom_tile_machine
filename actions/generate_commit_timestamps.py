import datetime
import random
from typing import Generator


def generate_working_dates(from_date: datetime.date, to_date: datetime.date, min_days_per_week: int, max_days_per_week: int, include_weekends: bool) -> Generator[datetime.date, None, None]:
    """
    Generate a sequence of working dates within a specified range.

    Args:
        from_date (datetime.date): The start date of the range.
        to_date (datetime.date): The end date of the range.
        min_days_per_week (int): Minimum number of working days per week.
        max_days_per_week (int): Maximum number of working days per week.
        include_weekends (bool): Whether to include weekends as valid working days.

    Yields:
        datetime.date: A date representing a working day.
    """
    new_week = True
    num_days_any_week = include_weekends and 7 or 5
    num_days_this_week = 0
    days_choice = []

    current_date = from_date
    while current_date <= to_date:
        # At the start of each week we want to recalculate our random sample
        if current_date.weekday() == 0:
            new_week = True

        if new_week:
            # We chose a sample of a random amount from the valid days, weekends are excluded here if required
            new_week = False
            num_days_this_week = random.randint(min_days_per_week, min(max_days_per_week, num_days_any_week))
            days_choice = random.sample(range(num_days_any_week), num_days_this_week)

        # Skip any days we don't want to commit on
        if current_date.weekday() not in days_choice:
            current_date += datetime.timedelta(days=1)
            continue

        yield current_date
        current_date += datetime.timedelta(days=1)


def generate_commit_times(min_per_day: int, max_per_day: int, include_out_of_hours: bool) -> Generator[datetime.time, None, None]:
    """
    Generate a sequence of commit times for a single day.

    Args:
        min_per_day (int): Minimum number of commits per day.
        max_per_day (int): Maximum number of commits per day.
        include_out_of_hours (bool): Whether to include times outside standard working hours.

    Yields:
        datetime.time: A time representing a commit.
    """
    earliest_hour = include_out_of_hours and 0 or 9
    latest_hour = include_out_of_hours and 23 or 17

    num_commits = random.randint(min_per_day, max_per_day)
    commit_times = []

    for _ in range(num_commits):
        # Generate a random time for the commit
        commit_time = datetime.time(
            # Dev's opinionated choice - focus commits around shortly after lunch
            max(earliest_hour, min(int(random.gauss(14, 2)), latest_hour)),
            random.randint(0, 59),
            random.randint(0, 59),
        )

        commit_times.append(commit_time)

    # Sort the commit times to ensure they are in order
    commit_times.sort()

    for commit_time in commit_times:
        yield commit_time


def generate_commit_timestamps(from_date: datetime.date, to_date: datetime.date, min_days_per_week: int, max_days_per_week: int, include_weekends: bool, min_per_day: int, max_per_day: int, include_out_of_hours: bool) -> Generator[datetime.datetime, None, None]:
    """
    Generate a sequence of commit timestamps within a specified date range.

    Args:
        from_date (datetime.date): The start date of the range.
        to_date (datetime.date): The end date of the range.
        min_days_per_week (int): Minimum number of working days per week.
        max_days_per_week (int): Maximum number of working days per week.
        include_weekends (bool): Whether to include weekends as valid working days.
        min_per_day (int): Minimum number of commits per day.
        max_per_day (int): Maximum number of commits per day.
        include_out_of_hours (bool): Whether to include times outside standard working hours.

    Yields:
        datetime.datetime: A timestamp representing a commit.
    """
    for date in generate_working_dates(from_date, to_date, min_days_per_week, max_days_per_week, include_weekends):
        for time in generate_commit_times(min_per_day, max_per_day, include_out_of_hours):
            yield datetime.datetime.combine(date, time)
