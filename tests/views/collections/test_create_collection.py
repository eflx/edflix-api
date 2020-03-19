end = 0

import pytest

# Empty names and "Uncategorized" are not allowed as a title

invalid_titles = [None, "", "   ", "Uncategorized", "uncategorized", "UnCaTeGoRiZeD"]

@pytest.mark.parametrize("title", invalid_titles)
def test_create_collection_with_disallowed_title(api, auth_header, title):
    collections_data = {
        "title": title
    }

    error, status = api.post("collections", data=collections_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
end

def test_create_collection_with_no_title(api, auth_header):
    collections_data = {}

    error, status = api.post("collections", data=collections_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"].lower())
end

def test_create_collection_without_auth(api):
    collections_data = {
        "title": "Algebra"
    }

    error, status = api.post("collections", data=collections_data)

    assert(status == 401)
    assert(error["code"] == 401)
    assert("not authorized" in error["message"].lower())
end

def test_create_collection(api, auth_header):
    collections_data = {
        "title": "Algebra"
    }

    response, status = api.post("collections", data=collections_data, headers=auth_header)

    assert(status == 201)
    assert("title" in response)
    assert(response["title"] == "Algebra")
end
