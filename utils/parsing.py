import datetime
from pathlib import Path
import re
from typing import Callable

import click


def parse_directory() -> Callable:
    def parse(value: str) -> str:
        # Convert to Path object
        repo_path = Path(value).resolve()

        # Validate name
        if not repo_path.name or not repo_path.name.isascii():
            raise click.BadParameter("Invalid directory name. Must be ascii")

        # Validate path
        if repo_path.exists():
            raise click.BadParameter("Invalid directory. Must not exist")

        return value

    return parse


def parse_string(regex: re.Pattern) -> Callable:
    """
    A function to parse a string based on a given regex pattern.

    Args:
        regex (re.Pattern): The regex pattern to validate the string.

    Returns:
        Callable: A function that parses the string and checks if it matches the regex.
    """

    def parse(value: str) -> str:
        if not regex.match(value):
            raise click.BadParameter(f"Invalid value. Must match {regex.pattern}")

        return value

    return parse


def parse_date(min: datetime.date, max: datetime.date) -> Callable:
    def parse(value: str) -> datetime.date:
        try:
            parsed_values = datetime.date.fromisoformat(value)
        except ValueError:
            raise click.BadParameter("Invalid date format. Must be iso8601 format")

        if parsed_values < min or parsed_values > max:
            raise click.BadParameter(f"Date must be between {min} and {max}")

        return parsed_values

    return parse


def parse_int(min: int, max: int) -> Callable:
    def parse(value: str) -> int:
        try:
            parsed_value = int(value)
        except ValueError:
            raise click.BadParameter("Invalid value. Must be an integer")

        if parsed_value < min or parsed_value > max:
            raise click.BadParameter(f"Value must be between {min} and {max}")

        return parsed_value

    return parse


def parse_bool() -> Callable:
    def parse(value: str) -> bool:
        if value.lower() in ["true", "1"]:
            return True
        elif value.lower() in ["false", "0"]:
            return False
        else:
            raise click.BadParameter("Invalid value. Must be true or false")

    return parse
