import sys

def ensure_encoding(encoding='utf-8'):
    # Check the current encoding of the standard output
    if sys.stdout.encoding.lower() != encoding:
        print(f"Changing system encoding from {sys.stdout.encoding} to {encoding.upper()}.")
        # Reconfigure the standard output encoding to UTF-8
        sys.stdout.reconfigure(encoding=encoding)
    else:
        print(f"System encoding is already {encoding.upper()}")

ensure_encoding(encoding='cp1252')