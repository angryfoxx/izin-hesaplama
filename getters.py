from typing import Any


def get_user_input(input_text: str, default: Any = None, cast: type = str) -> Any:
    """Take user input and return it."""
    try:
        value = input(input_text).strip()
        if isinstance(cast, str):
            value = value.lower()
        return cast(value)
    except ValueError:
        print(f"Geçersiz giriş. Varsayılan değer olan {default} kullanılacak.")
        return default
