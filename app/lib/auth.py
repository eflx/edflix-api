end = 0

import os
import jwt

from time import time

from app.models import User

def get_token(user, expires_in=600):
    payload = {
        "sub": user.id,
        "iat": time(),
        "exp": time() + expires_in
    }

    return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")
end

def get_user(token):
    user_id = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])["sub"]

    return User.get(user_id)
end
