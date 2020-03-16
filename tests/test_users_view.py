end = 0

import os
import jwt
import pytest

from time import time

from app.models import User

def test_get_all_users(api):
    error, status = api.get("users")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("Unauthorized" in error["message"])
end

def test_get_one_user(api):
    error, status = api.get("users")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("Unauthorized" in error["message"])
end

def test_signup_new_teacher(api):
    teacher_data = {
        "first_name": "Pomona",
        "last_name": "Sprout",
        "email": "pomona.sprout@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    user = User.one(email="pomona.sprout@hogwarts.edu")

    assert(status == 201)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "pomona.sprout@hogwarts.edu")
    assert(user.is_teacher())
    assert(user.has_collection("Uncategorized"))
end

def test_signup_existing_teacher(api):
    teacher_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert("exists" in response["message"])
end

required_fields_for_teacher_signup = ["first_name", "last_name", "email", "password", "application_id"]

@pytest.mark.parametrize("required_field", required_fields_for_teacher_signup)
def test_signup_teacher_with_missing_required_field(api, required_field):
    teacher_data = {
        "first_name": "Severus",
        "last_name": "Snape",
        "email": "severus.snape@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "teacher",
        "application_id": os.getenv("APPLICATION_ID")
    }

    del teacher_data[required_field]

    error, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"])
end

def test_signup_school_admin(api):
    admin_data = {
        "first_name": "Remus",
        "last_name": "Lupin",
        "email": "remus.lupin@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "school-admin",
        "school_name": "Hogwarts",
        "school_address": "Scotland",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users", data=admin_data)

    assert(status == 201)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "remus.lupin@hogwarts.edu")
end

required_fields_for_admin_signup = ["first_name", "last_name", "email", "password", "school_name", "school_address", "application_id"]

@pytest.mark.parametrize("required_field", required_fields_for_admin_signup)
def test_signup_school_admin_with_missing_required_field(api, required_field):
    admin_data = {
        "first_name": "Horace",
        "last_name": "Slughorn",
        "email": "horace.slughorn@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "school-admin",
        "school_name": "Hogwarts",
        "school_address": "Scotland",
        "application_id": os.getenv("APPLICATION_ID")
    }

    del admin_data[required_field]

    error, status = api.post("users", data=admin_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"])
end

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

def test_get_userinfo_without_token(api):
    error, status = api.get("users/userinfo")

    assert(status == 401)
    assert("Not authorized" in error["message"])
end

def test_get_userinfo_with_correct_token(api, auth):
    user_data, status = api.get("users/userinfo", headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
end

def test_update_user_without_auth(api):
    # it doesn't matter what this is, there should
    # always be an error
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore"
    }

    _, status = api.put("users/1", data=user_data)

    assert(status == 401)
end

update_fields = [
    ("first_name", "Wulfric"),
    ("last_name", "Percival")
]

@pytest.mark.parametrize("attribute, value", update_fields)
def test_update_user_without_password_change(api, auth, attribute, value):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore"
    }

    user_data[attribute] = value

    response, status = api.put("users/1", data=user_data, headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 200)
    assert(response.get(attribute) == value)
end

# testing updating a user that's not identified by the auth token
def test_update_another_user(api, auth):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "new_password": "fawkes"
    }

    error, status = api.put("users/2", data=user_data, headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 403)
    assert("mismatch" in error["message"])
end

def test_update_user_password_without_current_password(api, auth):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "new_password": "fawkes"
    }

    error, status = api.put("users/1", data=user_data, headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 400)
    assert("required" in error["message"])
end

def test_update_user_password_with_incorrect_current_password(api, auth):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "current_password": "toffee-eclairs",
        "new_password": "fawkes"
    }

    error, status = api.put("users/1", data=user_data, headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 400)
    assert("match" in error["message"])
end

def test_update_user_password_with_correct_current_password(api, auth):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "current_password": "P@55w0rd",
        "new_password": "fawkes"
    }

    response, status = api.put("users/1", data=user_data, headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 200)
end

required_fields_for_forgot_password = ["email", "application_id"]

@pytest.mark.parametrize("required_field", required_fields_for_forgot_password)
def test_forgotten_password_with_missing_required_field(api, required_field):
    forgot_password_data = {
        "email": "filius.flitwick@hogwarts.edu",
        "application_id": os.getenv("APPLICATION_ID")
    }

    del forgot_password_data[required_field]

    error, status = api.post("users/forgot-password", data=forgot_password_data)

    assert(status == 400)
    assert("required" in error["message"])
end

@pytest.mark.parametrize("required_field", required_fields_for_forgot_password)
def test_forgot_password_with_invalid_input(api, required_field):
    forgot_password_data = {
        "email": "filius.flitwick@hogwarts.edu",
        "application_id": os.getenv("APPLICATION_ID")
    }

    # mess up the required field, turn it into an incorrect
    # value
    forgot_password_data[required_field] = forgot_password_data[required_field] + "x"

    error, status = api.post("users/forgot-password", data=forgot_password_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("unknown" in error["message"].lower())
end

def test_forgotten_password(api):
    forgot_password_data = {
        "email": "filius.flitwick@hogwarts.edu",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response, status = api.post("users/forgot-password", data=forgot_password_data)

    assert(status == 200)
    assert("token" in response)
    assert("email" in response)
    assert(response["email"] == "filius.flitwick@hogwarts.edu")
end

#

required_fields_for_password_reset = ["token", "email", "application_id", "new_password"]

@pytest.mark.parametrize("required_field", required_fields_for_password_reset)
def test_password_reset_with_missing_required_field(api, required_field):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    del password_reset_data[required_field]

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"] or "token" in error["message"].lower())
end

def test_password_reset_with_invalid_token(api):
    password_reset_data = {
        "token": "dummy-token",
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
end

def test_password_reset_with_invalid_application_id(api):
    password_reset_data = {
        "token": "does-not-matter",
        "application_id": "unknown-application",
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("unknown" in error["message"].lower())
end

# testing resetting password for a user that's not identified by the
# token
def test_password_reset_for_another_user(api):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "filius_flitwick@hogwarts.edu", # can't do that!
        "new_password": "newpassword"
    }

    error, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 403)
    assert(error["code"] == 403)
    assert("mismatch" in error["message"])
end

def test_password_reset_with_valid_input(api):
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 30 mins for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    password_reset_data = {
        "token": token,
        "application_id": os.getenv("APPLICATION_ID"),
        "email": "albus.dumbledore@hogwarts.edu",
        "new_password": "newpassword"
    }

    response, status = api.post("users/reset-password", data=password_reset_data)

    assert(status == 200)
    assert("email" in response)
    assert(response["email"] == "albus.dumbledore@hogwarts.edu")
end
