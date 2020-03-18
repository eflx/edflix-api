end = 0

import os
import pytest

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
def test_forgotten_password_with_invalid_input(api, required_field):
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
