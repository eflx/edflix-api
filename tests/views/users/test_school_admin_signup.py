end = 0

import os
import pytest

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
