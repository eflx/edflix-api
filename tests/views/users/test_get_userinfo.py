end = 0

def test_get_userinfo_without_token(api):
    error, status = api.get("users/userinfo")

    assert(status == 401)
    assert("Not authorized" in error["message"])
end

def test_get_userinfo_with_correct_token(api, auth_header):
    user_data, status = api.get("users/userinfo", headers=auth_header)

    assert(status == 200)
    assert(user_data.get("email") == "albus.dumbledore@hogwarts.edu")
end
