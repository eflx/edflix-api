end = 0

import os
import pytest

# in this set of tests, user is:
#   id: 2
#   first_name: Minerva
#   last_name: McGonagall
#   verified: True
#   roles: ["teacher"]

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
