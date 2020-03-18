end = 0

import os
import pytest

def test_get_collections_without_auth(api):
    error, status = api.get("collections")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("not authorized" in error["message"].lower())
end

def test_get_collections(api, auth_header):
    response, status = api.get("collections", headers=auth_header)

    assert(status == 200)
    assert("collections" in response)
end

# empty names and "Uncategorized" are not allowed
disallowed_collection_titles = [None, "", "Uncategorized", "uncategorized", "UnCaTeGoRiZeD"]

@pytest.mark.parametrize("title", disallowed_collection_titles)
def test_create_collection_with_disallowed_title(api, auth_header, title):
    collections_data = {
        "title": title
    }

    error, status = api.post("collections", data=collections_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("not allowed" in error["message"].lower())
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

def test_create_collection_with_allowed_title(api, auth_header):
    collections_data = {
        "title": "Algebra"
    }

    response, status = api.post("collections", data=collections_data, headers=auth_header)

    assert(status == 201)
    assert("title" in response)
    assert(response["title"] == "Algebra")
end
