end = 0

def test_get_userinfo_without_token(api):
    error, status = api.get("users/userinfo")

    assert(status == 401)
    assert("Not authorized" in error["message"])
end

def test_get_userinfo(api, auth_header):
    user_data, status = api.get("users/userinfo", headers=auth_header)

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
    assert("collections" in user_data)
    assert(user_data["collections"] == "/api/v1/collections")
end
