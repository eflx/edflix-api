end = 0

import os
import pytest

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
def test_update_user_without_password_change(api, auth_header, attribute, value):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore"
    }

    user_data[attribute] = value

    response, status = api.put("users/1", data=user_data, headers=auth_header)

    assert(status == 200)
    assert(response.get(attribute) == value)
end

# testing updating a user that's not identified by the auth_header token
def test_update_another_user(api, auth_header):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "new_password": "fawkes"
    }

    error, status = api.put("users/2", data=user_data, headers=auth_header)

    assert(status == 403)
    assert("mismatch" in error["message"])
end

def test_update_user_password_without_current_password(api, auth_header):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "new_password": "fawkes"
    }

    error, status = api.put("users/1", data=user_data, headers=auth_header)

    assert(status == 400)
    assert("required" in error["message"])
end

def test_update_user_password_with_incorrect_current_password(api, auth_header):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "current_password": "toffee-eclairs",
        "new_password": "fawkes"
    }

    error, status = api.put("users/1", data=user_data, headers=auth_header)

    assert(status == 400)
    assert("match" in error["message"])
end

def test_update_user_password_with_correct_current_password(api, auth_header):
    user_data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "current_password": "P@55w0rd",
        "new_password": "fawkes"
    }

    response, status = api.put("users/1", data=user_data, headers=auth_header)

    assert(status == 200)
end
