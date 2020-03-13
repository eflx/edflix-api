end = 0

import os
import pytest

# in this set of tests, user is:
#   id: 1
#   first_name: Minerva
#   last_name: McGonagall
#   verified: True
#   roles: ["teacher"]

def get_role_names(roles):
    return list(map(lambda role: role.name, roles))
end

def test_add_invalid_role(user):
    user.add_role("mugwump")

    assert("mugwump" not in get_role_names(user.roles))
end

def test_add_existing_role(user):
    user.add_role("teacher")

    assert(len(user.roles) == 1) # should still be the original one
end

def test_add_valid_role(user):
    user.add_role("school-admin")

    assert(len(user.roles) == 2)
    assert("school-admin" in get_role_names(user.roles))
end

# empty names and "Uncategorized" are not allowed
disallowed_collection_names = [None, "", "Uncategorized", "uncategorized", "UnCaTeGoRiZeD"]

@pytest.mark.parametrize("name", disallowed_collection_names)
def test_create_collection_with_disallowed_name(user, name):
    with pytest.raises(ValueError):
        collection = user.create_collection(name)
    end
end

def test_create_collection_with_allowed_name(user):
    collection = user.create_collection("Algebra")

    assert(collection.id is not None)
    assert(collection.title == "Algebra")
    assert(collection.user_id == user.id)
end
