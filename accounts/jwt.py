import jwt

from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_tokens(user):
    now = datetime.now(timezone.utc)

    access_payload = {
        "user_id": user.id,
        "email": user.email,
        "type": "access",
        "exp": now + timedelta(minutes=15),
        "iat": now,
    }

    refresh_payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": now + timedelta(days=7),
        "iat": now,
    }

    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        refresh_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "access": access_token,
        "refresh": refresh_token,
    }