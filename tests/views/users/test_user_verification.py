end = 0

import os
import jwt

from time import time

def test_user_verification_without_token(api):
    data = {}

    error, status = api.post("users", data=data)

    assert(status == 400)
    assert("required" in error["message"])
end

def test_user_verification_with_valid_input(api):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 24 hours for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID")
    }

    user_data, status = api.post("users/verify", data=data)

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
end

# application id is checked before the token, so if we're checking for
# invalid token, we have to give the correct application id
def test_user_verification_with_invalid_token(api):
    data = {
        "token": "dummy-token",
        "application_id": os.getenv("APPLICATION_ID")
    }

    _, status = api.post("users/verify", data=data)

    assert(status == 400)
end

def test_user_verification_with_invalid_application_id(api):
    data = {
        "token": "dummy-token",
        "application_id": "dummy-application-id"
    }

    error, status = api.post("users/verify", data=data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("unknown" in error["message"].lower())
end
