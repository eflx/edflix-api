end = 0

import pytest

from app.models import Collection

def test_update_collection_with_no_title(api, collection, auth_header):
    collection_data = {}

    error, status = api.put(f"collections/{collection.id}", data=collection_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("required" in error["message"].lower())
end

def test_update_nonexistent_collection(api, auth_header):
    collection_data = {
        "title": "The Dursleys"
    }

    error, status = api.put(f"collections/2020", data=collection_data, headers=auth_header)

    assert(status == 404)
    assert(error["code"] == 404)
    assert("not found" in error["message"].lower())
end

def test_update_collection_without_auth(api, collection):
    collection_data = {
        "title": "Arithmancy"
    }

    error, status = api.put(f"collections/{collection.id}", data=collection_data)

    assert(status == 401)
    assert(error["code"] == 401)
    assert("not authorized" in error["message"].lower())
end

def test_update_collection_with_title_of_another_collection(api, collection, auth_header):
    collection_data = {
        "title": "Uncategorized" # safe to use this, because
        # this collection always exists
    }

    error, status = api.put(f"collections/{collection.id}", data=collection_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("exists" in error["message"].lower())
end

def test_update_collection_of_another_user(api, collection, auth_header):
    collection = Collection.one(title="Charms", user_id=3) # flitwick (id=3)
    # has a collection called Charms...

    collection_data = {
        "title": "Jinxes"
    }

    # ...but the authorization is for dumbledore (id=1)
    error, status = api.put(f"collections/{collection.id}", data=collection_data, headers=auth_header)

    assert(status == 403)
    assert(error["code"] == 403)
    assert("mismatch" in error["message"].lower())
end

def test_update_uncategorized_collection(api, uncategorized_collection, auth_header):
    collection_data = {
        "title": "Clutter"
    }

    error, status = api.put(f"collections/{uncategorized_collection.id}", data=collection_data, headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("not allowed" in error["message"])
end

def test_update_collection(api, collection, auth_header):
    collections_data = {
        "title": "Arithmancy"
    }

    response, status = api.put(f"collections/{collection.id}", data=collections_data, headers=auth_header)

    assert(status == 200)
    assert("id" in response)
    assert("url" in response)
    assert("title" in response)
    assert(response["title"] == "Arithmancy")
end
