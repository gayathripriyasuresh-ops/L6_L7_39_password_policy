def first_character_type(pw):
    """Classify the first character of a non-empty password string.

    Returns 'digit', 'letter', 'whitespace', or 'symbol' for valid non-empty
    strings, and None for non-string or empty inputs.
    """
    if not isinstance(pw, str) or not pw:
        return None
    ch = pw[0]
    if ch.isdigit():
        return 'digit'
    if ch.isalpha():
        return 'letter'
    if ch.isspace():
        return 'whitespace'
    return 'symbol'


def split_credentials(text):
    """Split a 'user:password' string into a stripped (user, password) tuple.

    Splits on the first colon so passwords containing colons remain intact.
    Returns None if text is not a string, lacks ':', or has an empty user/password.
    """
    if not isinstance(text, str) or ':' not in text:
        return None
    user, password = text.split(':', 1)
    user = user.strip()
    password = password.strip()
    if not user or not password:
        return None
    return user, password


def digit_ratio(pw):
    """Return the fraction of digit characters in pw as a float in [0.0, 1.0].

    Returns 0.0 for empty or non-string inputs.
    """
    if not isinstance(pw, str) or not pw:
        return 0.0
    return sum(c.isdigit() for c in pw) / len(pw)


def main():
    """Run interactive CLI prompts for each password policy helper."""
    try:
        print("==== Running first_character_type ====")
        user_input = input("Enter a password: ")
        result = first_character_type(user_input)
        print(
            "First Character Type:",
            result if result is not None else "Invalid (empty or non-string input)",
        )

        print("\n==== Running split_credentials ====")
        user_input = input("Enter user:password (e.g. alice:Secret1): ")
        result = split_credentials(user_input)
        print(
            "User and Password:",
            result if result is not None else "Invalid format (expected non-empty user:password)",
        )

        print("\n==== Running digit_ratio ====")
        user_input = input("Enter a password to measure: ")
        result = digit_ratio(user_input)
        print("Digit Ratio:", result)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")


if __name__ == "__main__":
    main()
