end = 0

import os
import jwt
import pytest

def test_login(api):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    response, status = api.post("auth/token", data=login_data)

    assert(status == 200)
    assert("token" in response)

    try:
        token = jwt.decode(response["token"], os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError as e:
        token = None
    end

    assert(token is not None)
    assert("sub" in token)
    assert("iat" in token)
    assert("exp" in token)
    assert(int(token["exp"] - token["iat"]) == 10*24*60*60)
end

required_fields_for_login = ["email", "password"]

@pytest.mark.parametrize("required_field", required_fields_for_login)
def test_login_with_missing_fields(api, required_field):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    del login_data[required_field]

    error, status = api.post("auth/token", data=login_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"])
end

@pytest.mark.parametrize("required_field", required_fields_for_login)
def test_login_with_incorrect_credentials(api, required_field):
    login_data = {
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd"
    }

    # mess up the required field, turn it into an incorrect
    # value
    login_data[required_field] = login_data[required_field] + "x"

    error, status = api.post("auth/token", data=login_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("incorrect" in error["message"])
end

def test_login_for_unverified_user(api):
    login_data = {
        "email": "gilderoy.lockhart@hogwarts.edu",
        "password": "P@55w0rd"
    }

    error, status = api.post("auth/token", data=login_data)

    assert(status == 403)
end
