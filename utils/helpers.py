import logging
from pathlib import Path
from typing import List, Optional


def validate_args(args) -> bool:
    """
    Validate command-line arguments before doing any API calls.
    """
    credentials_path = Path(args.credentials)
    if not credentials_path.exists():
        logging.error("Credentials file not found at %s", credentials_path)
        return False

    if args.limit is not None and args.limit <= 0:
        logging.error("--limit must be greater than zero.")
        return False

    if args.front_field_name.strip() == args.back_field_name.strip():
        logging.error("Front and back field names must be different.")
        return False

    if normalize_header(args.front_column) == normalize_header(args.back_column):
        logging.error("Front and back columns must be different.")
        return False

    return True


def normalize_header(value: str) -> str:
    """
    Normalize a header string for case-insensitive comparisons.
    """
    return "".join(str(value).strip().lower().split())


def get_value_by_header(row: dict, header: str):
    """
    Fetch a value from a row using case-insensitive header matching.
    """
    normalized_target = normalize_header(header)
    for key, value in row.items():
        if normalize_header(key) == normalized_target:
            return value
    return None


def normalize_tags(tags: Optional[List[str]]) -> List[str]:
    """
    Clean up user-provided tags.
    """
    if not tags:
        return []
    cleaned = []
    for tag in tags:
        stripped = tag.strip()
        if stripped:
            cleaned.append(stripped)
    return cleaned
