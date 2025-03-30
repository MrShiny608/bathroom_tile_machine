import datetime
import re
import click
from typing import Any, Callable
import yaml
from functools import wraps

import utils.parsing as parsing
from actions.create_repo import create_repo
from actions.generate_commit_timestamps import generate_commit_timestamps
from actions.generate_commit_message import generate_commit_message
from git.git import Git
from git.config import get_user_name, get_user_email


class Config(object):
    """
    A class to handle configuration data loaded from a YAML file.

    This class provides methods to access configuration data using dictionary-like
    syntax and checks for the existence of keys.

    Methods:
        __init__():
            Initializes the Config object by loading data from a ".config.yaml" file.

        __getitem__(key: str) -> Any:
            Retrieves the value associated with the given key from the configuration data.
            Args:
                key (str): The key to look up in the configuration data.
            Returns:
                Any: The value associated with the key, or None if the key does not exist.

        __contains__(key: str) -> bool:
            Checks if a given key exists in the configuration data.
            Args:
                key (str): The key to check for existence.
            Returns:
                bool: True if the key exists, False otherwise.
    """

    def __init__(self):
        with open(".config.yaml", "r") as file:
            self.data = yaml.safe_load(file)

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self.data


def resolve_parameter(config_key: str, description: str, default: Callable, parser: Callable) -> Callable:
    """
    A decorator to resolve parameter values based on a precedence order:
    1. Command line parameter
    2. Configuration file
    3. Prompt user for input
    4. Default value

    Args:
        config_key (str): The key to look up in the configuration file.
        description (str): The message to display when describing the input.
        default (Any): The default value to use if no input is provided.

    Returns:
        Callable: A decorator function that wraps the target function.
    """

    def decorator(func: Callable) -> Callable:
        # Wrap the function with click.option to handle command-line arguments
        func = click.option(f"--{config_key.replace('_', '-')}", help=description, default=None)(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # If the command-line parameter is provided, use it
            if kwargs.get(config_key) is None:
                # Otherwise, load the configuration file and resolve the parameter
                ctx = click.get_current_context()
                config = ctx.ensure_object(Config)

                if config_key in config and config[config_key] is not None:
                    # If the config file has the parameter, use that
                    kwargs[config_key] = config[config_key]
                else:
                    # Otherwise, prompt the user for input as config file doesn't have the parameter
                    default_value = default()

                    kwargs[config_key] = click.prompt(
                        f"Please enter {description}",
                        type=type(default_value),
                        default=default_value,
                    )

            # Parse the parameter using the provided parser function
            try:
                # We convert to string as cli parameters will arrive as strings, but config files wouldn't
                # so stringify for consistency
                kwargs[config_key] = parser(str(kwargs[config_key]))
            except Exception as e:
                raise click.BadParameter(f"Invalid value for {config_key}: {e}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


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
    default=lambda: 4,
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
    default=lambda: 5,
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

    # Call the function to create the repository
    initial_commit_datetime = datetime.datetime.combine(from_date, datetime.datetime.now().time())
    create_repo(git, name, directory, initial_commit_datetime)

    # Generate the fake commits
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
        # Generate a commit message
        message = generate_commit_message()

        # Finally, commit it
        git.commit(commit_timestamp, message)


if __name__ == "__main__":
    main()
