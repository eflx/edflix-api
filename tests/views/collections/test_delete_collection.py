end = 0

import pytest

from app.models import Collection

def test_delete_nonexistent_collection(api, auth_header):
    error, status = api.delete(f"collections/2020", headers=auth_header)

    assert(status == 404)
    assert(error["code"] == 404)
    assert("not found" in error["message"].lower())
end

def test_delete_collection_without_auth(api, collection):
    error, status = api.delete(f"collections/{collection.id}")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("not authorized" in error["message"].lower())
end

def test_delete_collection_of_another_user(api, collection, auth_header):
    collection = Collection.one(title="Charms", user_id=3) # flitwick (id=3)
    # has a collection called Charms...

    # ...but the authorization is for dumbledore (id=1)
    error, status = api.delete(f"collections/{collection.id}", headers=auth_header)

    assert(status == 403)
    assert(error["code"] == 403)
    assert("mismatch" in error["message"].lower())
end

def test_delete_uncategorized_collection(api, uncategorized_collection, auth_header):
    error, status = api.delete(f"collections/{uncategorized_collection.id}", headers=auth_header)

    assert(status == 400)
    assert(error["code"] == 400)
    assert("not allowed" in error["message"])
end

def test_delete_collection(api, collection, auth_header):
    response, status = api.delete(f"collections/{collection.id}", headers=auth_header)

    assert(status == 204)
end
