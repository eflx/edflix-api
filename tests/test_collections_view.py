end = 0

import os
import pytest

def test_get_collections_without_auth(api):
    error, status = api.get("collections")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("Unauthorized" in error["message"])
end

def test_get_collections(api, auth):
    response, status = api.get("collections", headers={ "Authorization": f"Bearer {auth['token']}" })

    assert(status == 200)
    assert("collections" in response)
end
