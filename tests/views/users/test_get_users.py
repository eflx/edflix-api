end = 0

def test_get_all_users(api):
    error, status = api.get("users")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("Unauthorized" in error["message"])
end

def test_get_one_user(api):
    error, status = api.get("users")

    assert(status == 401)
    assert(error["code"] == 401)
    assert("Unauthorized" in error["message"])
end
