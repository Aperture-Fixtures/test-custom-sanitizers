import re

def is_valid_file_id(file_id: str) -> bool:
    """CodeQL Custom Sanitizer - validate file_id matches alphanumeric pattern."""
    return bool(re.match("^[A-Za-z0-9]+$", file_id))
