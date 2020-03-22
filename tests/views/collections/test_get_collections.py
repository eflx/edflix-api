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
