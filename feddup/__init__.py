"""
Fed-Dup - Federated Repository Duplication Engine
A lightweight, dependency-free Git mirroring tool built with Python and Streamlit.
"""

__version__ = "1.0.0"
__author__ = "Fed-Dup Team"
__license__ = "MIT"

from feddup.engine import duplicate_repository  # noqa: E402, F401
from feddup.config import (  # noqa: E402, F401
    load_config,
    save_config,
    add_repository,
    remove_repository,
    get_repository_count,
)
from feddup.utils import (  # noqa: E402, F401
    sanitize_git_url,
    validate_source_url,
    validate_destination_url,
    cleanup_workspace,
    get_repo_size,
)
from feddup.logger import get_logger  # noqa: E402, F401

__all__ = [
    "duplicate_repository",
    "load_config",
    "save_config",
    "add_repository",
    "remove_repository",
    "get_repository_count",
    "sanitize_git_url",
    "validate_source_url",
    "validate_destination_url",
    "cleanup_workspace",
    "get_repo_size",
    "get_logger",
    "__version__",
]
