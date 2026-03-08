"""
password_gen.py – Generate secure random passwords.
Usage: python password_gen.py [--length N] [--special] [--count N]
"""
import secrets
import string
import argparse


def generate_password(length: int = 12, use_special: bool = True) -> str:
    """Generate a cryptographically secure random password."""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation

    # Ensure at least one of each required type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]
    if use_special:
        password.append(secrets.choice(string.punctuation))

    remaining = length - len(password)
    password.extend(secrets.choice(chars) for _ in range(remaining))

    # Shuffle to avoid predictable positions
    result = list(password)
    secrets.SystemRandom().shuffle(result)
    return ''.join(result)


def main():
    parser = argparse.ArgumentParser(description='Secure password generator')
    parser.add_argument('--length', type=int, default=16, help='Password length')
    parser.add_argument('--special', action='store_true', help='Include special chars')
    parser.add_argument('--count', type=int, default=1, help='Number of passwords')
    args = parser.parse_args()

    for i in range(args.count):
        pw = generate_password(length=args.length, use_special=args.special)
        print(pw)


if __name__ == '__main__':
    main()
