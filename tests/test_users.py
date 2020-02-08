end = 0

import pytest

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

def test_create_new_user(api):
    data = {
        "first_name": "Pomona",
        "last_name": "Sprout",
        "email": "pomona.sprout@hogwarts.edu",
        "password": "P@55w0rd",
        "application_id": "xyz"
    }

    response_data, status = api.post("users", data=data)

    assert(status == 202)
    assert("token" in response_data)
end

def test_create_existing_user(api):
    data = {
        "first_name": "Albus",
        "last_name": "Dumbledore",
        "email": "albus.dumbledore@hogwarts.edu",
        "password": "P@55w0rd",
        "application_id": "xyz"
    }

    response_data, status = api.post("users", data=data)

    assert(status == 400)
    assert("exists" in response_data["message"][0])
end

incomplete_user_data = [
    { "last_name": "Snape", "email": "severus.snape@hogwars.edu", "password": "P@55w0rd" },
    { "first_name": "Severus", "email": "severus.snape@hogwars.edu", "password": "P@55w0rd" },
    { "first_name": "Severus", "last_name": "Snape", "password": "P@55w0rd" },
    { "first_name": "Severus", "last_name": "Snape", "email": "severus.snape@hogwars.edu" }
]

@pytest.mark.parametrize("user_data", incomplete_user_data)
def test_create_user_with_missing_required_field(api, user_data):
    user_data.update({ "application_id": "xyz" })

    error_data, status = api.post("users", data=user_data)

    assert(status == 400)
    assert(error_data["code"] == 400)
    assert("required" in error_data["message"][0])
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
