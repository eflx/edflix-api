end = 0

import os
import pytest

from app.models import User
from app.models import Collection

def test_create_collection(user):
    transfiguration = user.create_collection("Transfiguration")

    assert(transfiguration is not None)
    assert(transfiguration.id is not None)
    assert(transfiguration.user_id == user.id)
    assert(len(user.collections.all()) == 2)
    assert(user.has_collection("Transfiguration"))
end

# TODO: add more tests
