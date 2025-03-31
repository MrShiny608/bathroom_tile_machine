import datetime
import re
import click

from utils.parameters import resolve_parameter
import utils.parsing as parsing
from actions.create_repo import create_repo
from actions.generate_commit_timestamps import generate_commit_timestamps
from actions.generate_commit_message import generate_commit_message
from git.git import Git
from git.config import get_user_name, get_user_email


@click.command()
@resolve_parameter(
    config_key="username",
    description="the name of user who should be attributed to the commits",
    default=get_user_name,
    parser=parsing.parse_string(re.compile(r"^.*$")),  # Just a username, doesn't have to match anything?
)
@resolve_parameter(
    config_key="email",
    description="the email of user who should be attributed to the commits",
    default=get_user_email,
    parser=parsing.parse_string(re.compile(r"^.*@.*$")),  # Don't fight email addresses, you won't win
)
@resolve_parameter(
    config_key="name",
    description="the name of the new repository",
    default=lambda: "bathroom_tiles",
    parser=parsing.parse_string(re.compile(r"^[a-zA-Z0-9_\-.]{1,100}$")),
)
@resolve_parameter(
    config_key="directory",
    description="the directory where the repository will be created",
    default=lambda: "./bathroom_tiles",
    parser=parsing.parse_directory(),
)
@resolve_parameter(
    config_key="from_date",
    description="the date from which the commits should be attributed in iso8601 format",
    default=lambda: (datetime.date.today() - datetime.timedelta(weeks=52, days=1)).isoformat(),
    parser=parsing.parse_date(min=datetime.date(1970, 1, 1), max=datetime.date.today()),
)
@resolve_parameter(
    config_key="to_date",
    description="the date to which the commits should be attributed in iso8601 format",
    default=lambda: (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
    parser=parsing.parse_date(min=datetime.date(1970, 1, 1), max=datetime.date.today()),
)
@resolve_parameter(
    config_key="min_days_per_week",
    description="the minimum number of days per week",
    default=lambda: 3,
    parser=parsing.parse_int(min=1, max=7),
)
@resolve_parameter(
    config_key="max_days_per_week",
    description="the maximum number of days per week",
    default=lambda: 5,
    parser=parsing.parse_int(min=1, max=7),
)
@resolve_parameter(
    config_key="include_weekends",
    description="whether to include weekends in commit generation (true/false)",
    default=lambda: False,
    parser=parsing.parse_bool(),
)
@resolve_parameter(
    config_key="min_per_day",
    description="the minimum number of commits per day",
    default=lambda: 1,
    parser=parsing.parse_int(min=1, max=1000),
)
@resolve_parameter(
    config_key="max_per_day",
    description="the maximum number of commits per day",
    default=lambda: 10,
    parser=parsing.parse_int(min=1, max=1000),
)
@resolve_parameter(
    config_key="include_out_of_hours",
    description="whether to include out-of-hours commits (true/false)",
    default=lambda: True,
    parser=parsing.parse_bool(),
)
def main(
    username: str,
    email: str,
    name: str,
    directory: str,
    from_date: datetime.date,
    to_date: datetime.datetime,
    min_days_per_week: int,
    max_days_per_week: int,
    include_weekends: bool,
    min_per_day: int,
    max_per_day: int,
    include_out_of_hours: bool,
) -> None:
    # Initialise git object
    git = Git(
        username,
        email,
        name,
        directory,
    )

    # Generate the fake commits
    initial_commit = True
    for commit_timestamp in generate_commit_timestamps(
        from_date,
        to_date,
        min_days_per_week=min_days_per_week,
        max_days_per_week=max_days_per_week,
        include_weekends=include_weekends,
        min_per_day=min_per_day,
        max_per_day=max_per_day,
        include_out_of_hours=include_out_of_hours,
    ):
        if initial_commit:
            # First create the repository
            create_repo(git, name, directory, commit_timestamp)
            initial_commit = False
        else:
            # Generate a commit message
            message = generate_commit_message()

            # Finally, commit it
            git.commit(commit_timestamp, message)


if __name__ == "__main__":
    main()
