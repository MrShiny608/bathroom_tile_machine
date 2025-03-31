from typing import Any
import yaml


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
