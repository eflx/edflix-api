end = 0

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
    assert(len(response["collections"]) == 2) # the default "Uncategorized",
    # and "Transfiguration"
end

def test_get_single_collection_without_auth(api):
    error, status = api.get("collections/6") # collection (id=6) is
    # Transfiguration

    assert(status == 401)
    assert(error["code"] == 401)
    assert("not authorized" in error["message"].lower())
end

def test_get_nonexistent_collection(api, auth_header):
    error, status = api.get("collections/2020", headers=auth_header)

    assert(status == 404)
    assert(error["code"] == 404)
    assert("not found" in error["message"].lower())
end

def test_get_single_collection(api, auth_header):
    response, status = api.get("collections/6", headers=auth_header)

    assert(status == 200)
    assert("id" in response)
    assert("url" in response)
    assert("title" in response)
    assert(response["title"] == "Transfiguration")
end

