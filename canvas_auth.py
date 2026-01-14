import requests
from tkinter import simpledialog, messagebox
import token_canvas # Your TOKEN

BASE_URL = "YOUR DOMAIN"

_cached_headers = None


def validate_token(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(
            f"{BASE_URL}/api/v1/users/self",
            headers=headers,
            timeout=10
        )
        r.raise_for_status()
        return headers
    except Exception:
        return None


def prompt_for_token():
    """
    1. Try default token first
    2. If invalid, prompt user
    """
    global _cached_headers

    if _cached_headers:
        return _cached_headers

    # --- Try default token ---
    headers = validate_token(token_canvas.TOKEN_KEY)
    if headers:
        _cached_headers = headers
        return headers

    # --- Ask user ---
    token = simpledialog.askstring(
        "Canvas Access Token Required",
        "Default token is invalid or expired.\n\n"
        "Please enter your Canvas Access Token:",
        show="*"
    )

    if token is None:
        messagebox.showinfo("Cancelled", "Operation cancelled by user.")
        return None

    token = token.strip()
    if not token:
        messagebox.showerror("Invalid Token", "No token entered.")
        return None

    headers = validate_token(token)
    if not headers:
        messagebox.showerror("Invalid Token", "Token validation failed.")
        return None

    _cached_headers = headers
    return headers
