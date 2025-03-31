from functools import wraps
from typing import Callable
import click

from utils.config import Config


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
