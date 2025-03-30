import click
from typing import Any, Callable
import yaml
from functools import wraps

from actions.create_repo import create_repo
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


def resolve_parameter(config_key: str, description: str, default: Callable) -> Callable:
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
            if kwargs.get(config_key) is not None:
                return func(*args, **kwargs)

            # Otherwise, load the configuration file and resolve the parameter
            ctx = click.get_current_context()
            config = ctx.ensure_object(Config)

            # Check if the config file has the parameter
            if config_key in config and config[config_key] is not None:
                kwargs[config_key] = config[config_key]
                return func(*args, **kwargs)

            # We may need the default now, so call the default resolver function
            default_value = default()

            # Prompt the user for input as config file doesn't have the parameter
            kwargs[config_key] = click.prompt(f"Please enter {description}", type=type(default_value), default=default_value)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@click.command()
@resolve_parameter(
    config_key="username",
    description="the name of user who should be attributed to the commits",
    default=get_user_name,
)
@resolve_parameter(
    config_key="email",
    description="the email of user who should be attributed to the commits",
    default=get_user_email,
)
@resolve_parameter(
    config_key="repo_name",
    description="the name of the new repository",
    default=lambda: "bathroom_tiles",
)
@resolve_parameter(
    config_key="repo_directory",
    description="the directory where the repository will be created",
    default=lambda: "./bathroom_tiles",
)
def main(username: str, email: str, repo_name: str, repo_directory: str) -> None:
    # Initialise git object
    git = Git(
        username,
        email,
        repo_name,
        repo_directory,
    )

    # Call the function to create the repository
    create_repo(git, name=repo_name, directory=repo_directory)


if __name__ == "__main__":
    main()
