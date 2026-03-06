"""
Utilities for reading the graph data.
"""

import json
import os
from importlib import resources
from pathlib import Path

from .models import SupplyChainNetwork

DEFAULT_FILE_NAME = "take-home-example.json"
"""
The default file name for the supply chain data.
"""

ENV_VAR_FILE_NAME = "SUPPLY_CHAIN_DATA_FILE"
"""
The environment variable name for the supply chain data file.
"""


def file_in_data_folder(file_name: str | None = None) -> Path:
    """
    Get the default path to the supply chain data file.
    """
    with resources.path(
        "supply_chain_data",
        # Read file name in this specific order:
        # - provided file_name argument
        # - environment variable
        # - default file name
        file_name or os.environ.get(ENV_VAR_FILE_NAME, "") or DEFAULT_FILE_NAME,
    ) as path:
        return path.absolute()


def supply_chain_network_from_file(
    path: "Path | str | None" = None,
) -> SupplyChainNetwork:
    """
    Load the supply chain network from a file.

    This does not perform any validation on the data; please ensure the data is valid
    before calling this function.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    if path is None:
        path = file_in_data_folder()
    elif isinstance(path, str) or not path.is_absolute():
        path = file_in_data_folder(path.as_posix() if isinstance(path, Path) else path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path.as_posix()}")
    elif not path.is_file():
        raise FileNotFoundError(f"Path is not a file: {path.as_posix()}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

        return data
