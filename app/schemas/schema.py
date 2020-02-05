end = 0

from app import ma

from marshmallow import EXCLUDE
from marshmallow import post_dump
from marshmallow import validate

class Schema(ma.Schema):
    __envelope__ = None # use in subclasses to define
    # an envelope for wrapping a list in a namespace

    unknown = EXCLUDE

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        return { self.__envelope__: data } if many and self.__envelope__ else data
    end
end
