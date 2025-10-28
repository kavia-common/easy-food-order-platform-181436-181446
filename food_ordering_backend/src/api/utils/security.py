import hashlib
import hmac
import os


SALT = os.getenv("PASSWORD_SALT", "devsalt").encode("utf-8")


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Hash a password using HMAC-SHA256 with a static salt (for demo only)."""
    return hmac.new(SALT, password.encode("utf-8"), hashlib.sha256).hexdigest()


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password by comparing HMAC-SHA256 hash."""
    return hmac.new(SALT, plain_password.encode("utf-8"), hashlib.sha256).hexdigest() == hashed_password
