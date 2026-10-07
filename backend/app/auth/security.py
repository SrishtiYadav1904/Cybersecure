import datetime
from typing import Optional, Dict, Any
import hashlib
import hmac
import base64
import json
import os

# Check if passlib is installed
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    pwd_context = None

from backend.app.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if pwd_context is not None:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            pass
    # Universal salted SHA-256 fallback
    if ":" in hashed_password:
        salt, h = hashed_password.split(":", 1)
        check = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return check == h
    return False

def get_password_hash(password: str) -> str:
    if pwd_context is not None:
        try:
            return pwd_context.hash(password)
        except Exception:
            pass
    salt = os.urandom(16).hex()
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}:{h}"

# Robust Universal JWT Encoder/Decoder
def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def _b64url_decode(s: str) -> bytes:
    padding = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(s + padding)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})

    # Try jose/jwt if installed
    try:
        from jose import jwt
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception:
        pass

    try:
        import jwt
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception:
        pass

    # Pure Python HMAC-SHA256 JWT
    header = {"alg": "HS256", "typ": "JWT"}
    h_b64 = _b64url_encode(json.dumps(header).encode("utf-8"))
    p_b64 = _b64url_encode(json.dumps(to_encode).encode("utf-8"))
    signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
    sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64url_encode(sig)
    return f"{h_b64}.{p_b64}.{sig_b64}"

def decode_access_token(token: str) -> dict:
    try:
        from jose import jwt
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        pass

    try:
        import jwt
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        pass

    # Pure Python HMAC-SHA256 JWT Verifier
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format")

    h_b64, p_b64, sig_b64 = parts
    signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
    expected_sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_sig = _b64url_decode(sig_b64)

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("Signature verification failed")

    payload = json.loads(_b64url_decode(p_b64).decode("utf-8"))
    exp = payload.get("exp")
    if exp and datetime.datetime.utcnow().timestamp() > exp:
        raise ValueError("Token has expired")

    return payload
