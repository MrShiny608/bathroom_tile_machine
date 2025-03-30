import click
from typing import Optional, TypeVar
import yaml

from git import repo


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


T = TypeVar("T")


def load_parameter(
    config_file: dict,
    command_line: Optional[T],
    config_key: str,
    prompt: str,
    default: T,
) -> T:
    """
    Loads a parameter value based on a priority order: command line argument,
    configuration file, or user input prompt.

    Args:
        config_file (dict): A dictionary containing configuration key-value pairs.
        command_line (Optional[Any]): The value provided via the command line argument.
                                      This has the highest priority.
        config_key (str): The key to look up in the configuration file.
        prompt (str): The message to display when prompting the user for input.
        default (Optional[Any]): The default value to use if no input is provided.

    Returns:
        Any: The resolved parameter value based on the priority order.
    """

    # Command line argument is highest priority
    if command_line is not None:
        return command_line

    # Config file value is second priority
    if config_key in config_file:
        return config_file[config_key]

    # Prompt the user for input
    return click.prompt(prompt, type=type(default), default=default)


@click.command()
@click.option("--repo_name", help="The name of the new repository")
@click.option("--repo_directory", help="The directory where the repository will be created")
def create_repo(repo_name: str, repo_directory: str) -> None:
    """
    Create a new Git repository.
    """

    # Load the configuration file
    config = load_config(".config.yaml")

    # Get parameters
    repo_name = load_parameter(
        config,
        repo_name,
        config_key="repo_name",
        prompt="Please enter the name of the new repository",
        default="my_repo",
    )

    repo_directory = load_parameter(
        config,
        repo_directory,
        config_key="repo_directory",
        prompt="Please enter the directory where the repository will be created",
        default="./my_repo",
    )

    # Call the function to create the repository
    repo.create_repo(repo_name, repo_directory)


if __name__ == "__main__":
    create_repo()
