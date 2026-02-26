import re

# Username validation rules
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20

# Allow letters, digits and underscore, within the length range
USER_USERNAME_REGEX = re.compile(
    rf"^[A-Za-z0-9_]{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
)


def validate_username(raw_username: str) -> str:
    """Validate a username and return the cleaned value.

    Rules:
    - Required (non-empty after stripping)
    - Length between USER_USERNAME_MIN and USER_USERNAME_MAX
    - Only letters, digits and underscore

    Raises ValueError with a human-readable message on failure.
    """

    username = (raw_username or "").strip()

    if not username:
        raise ValueError("Username is required")

    if not USER_USERNAME_REGEX.fullmatch(username):
        raise ValueError(
            f"Username must be {USER_USERNAME_MIN}-{USER_USERNAME_MAX} characters, "
            "letters, numbers, or underscore only."
        )

    return username
