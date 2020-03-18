end = 0

import os
import pytest

from app.models import Role

# in this set of tests, user is:
#   id: 2
#   first_name: Minerva
#   last_name: McGonagall
#   verified: True
#   roles: ["teacher"]

def test_add_invalid_role(user):
    user.add_role("mugwump")

    assert("mugwump" not in user.role_names())
end

def test_add_existing_role(user):
    user.add_role("teacher")

    assert(len(user.roles) == 1) # should still be the original one
end

def test_add_valid_role(user):
    user.add_role("school-admin")

    assert(len(user.roles) == 2)
    assert("school-admin" in user.role_names())
end
