end = 0

import os
import jwt
import pytest

from time import time

def test_get_all_users(api):
    error_data, status = api.get("users")

    assert(status == 401)
    assert(error_data["code"] == 401)
    assert("Unauthorized" in error_data["message"])
end

def test_get_one_user(api):
    error_data, status = api.get("users")

    assert(status == 401)
    assert(error_data["code"] == 401)
    assert("Unauthorized" in error_data["message"])
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

    response_data, status = api.post("users", data=teacher_data)

    assert(status == 202)
    assert("email" in response_data)
    assert("token" in response_data)
    assert("roles" in response_data)
    assert("teacher" in response_data["roles"])
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

    response_data, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert("exists" in response_data["message"])
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

    error_data, status = api.post("users", data=teacher_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"])
end

def test_signup_school_admin(api):
    admin_data = {
        "first_name": "Filius",
        "last_name": "Flitwick",
        "email": "filuis.flitwick@hogwarts.edu",
        "password": "P@55w0rd",
        "role": "school-admin",
        "school_name": "Hogwarts",
        "school_address": "Scotland",
        "application_id": os.getenv("APPLICATION_ID")
    }

    response_data, status = api.post("users", data=admin_data)

    assert(status == 202)
    assert("email" in response_data)
    assert("token" in response_data)
    assert("roles" in response_data)
    assert("school-admin" in response_data["roles"])
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

    error_data, status = api.post("users", data=admin_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"])
end

def test_user_verification_without_token(api):
    data = {}

    error_data, status = api.post("users", data=data)

    assert(status == 400)
    assert("required" in error_data["message"])
end

def test_user_verification_with_valid_token(api):
    # test with dummy token -- all we're testing for
    # right now is that there *is* a token in the payload
    payload = {
        "sub": 1, # dumbledore user, id=1
        "iat": time(),
        "exp": time() + 1*60 # 24 hours for a real user; 1 min for testing
    }

    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256").decode("UTF-8")

    data = {
        "token": token
    }

    user_data, status = api.post("users/verify", data=data)

    assert(status == 200)
    assert(user_data["email"] == "albus.dumbledore@hogwarts.edu")
end

# def test_add_new_book_to_user(api):
#     data = {
#         "title": "Harry Potter and the Goblet of Fire"
#     }

#     book_data, status = api.post("users/1/books", data=data)

#     assert(status == 201)
#     assert(book_data["title"] == "Harry Potter and the Goblet of Fire")
#     assert(book_data["is_read"] == False)
# end

# def test_add_existing_book_to_user(api):
#     data = {
#         "book_id": 2
#     }

#     book_data, status = api.post("users/1/books", data=data)

#     assert(status == 201)
#     assert(book_data["title"] == "Harry Potter and the Chamber of Secrets")
#     assert(book_data["is_read"] == False)
# end

# @pytest.mark.parametrize("read_status", [True, False])
# def test_set_book_read(api, read_status):
#     data = {
#         "is_read": read_status
#     }

#     book_data, status = api.put("users/1/books/2", data)

#     assert(status == 200)
#     assert(book_data["url"] == "/api/v1/books/2")
#     assert(book_data["is_read"] == read_status)
# end

# @pytest.mark.parametrize("read_status", [True, False])
# def test_set_non_existent_book_read(api, read_status):
#     data = {
#         "is_read": read_status
#     }

#     error_data, status = api.put("users/1/books/10", data)

#     assert(status == 400)
#     assert(error_data["code"] == 400)
#     assert("not found" in error_data["message"])
# end

# @pytest.mark.parametrize("read_status", [True, False])
# def test_set_unowned_book_read(api, read_status):
#     data = {
#         "is_read": read_status
#     }

#     error_data, status = api.put("users/1/books/3", data)

#     assert(status == 400)
#     assert(error_data["code"] == 400)
#     assert("does not have" in error_data["message"])
# end

# @pytest.mark.parametrize("read_status", [True, False])
# def test_set_book_read_for_non_existent_user(api, read_status):
#     data = {
#         "is_read": read_status
#     }

#     error_data, status = api.put("users/10/books/3", data)

#     assert(status == 404)
#     assert(error_data["code"] == 404)
#     assert("not found" in error_data["message"])
# end

# def test_delete_existing_user(api):
#     user_data, status = api.delete("users/1")

#     assert(status == 204)
# end

# def test_delete_non_existent_user(api):
#     error_data, status = api.delete("users/10")

#     assert(status == 404)
#     assert(error_data["code"] == 404)
#     assert("not found" in error_data["message"])
# end
