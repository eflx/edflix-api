end = 0

import json

from app import db

from sqlalchemy.orm import class_mapper
from marshmallow import ValidationError

from app.schemas import schemas

class Model(db.Model):
    __abstract__ = True

    @classmethod
    def all(cls, **params):
        if params:
            return cls.query.filter_by(**params)
        end

        return cls.query.all()
    end

    @classmethod
    def find(cls, id):
        return cls.query.get(id)
    end

    @classmethod
    def one(cls, **params):
        return cls.all(**params).first()
    end

    @classmethod
    def new(cls, model_params, **extra_params):
        if not cls.__name__ in schemas:
            raise Exception(f"No schema is defined for class {cls.__name__}")
        end

        params = schemas[cls.__name__].load(model_params)
        params.update(extra_params)

        # filter out the params that are not part of the class model
        # (otherwise you'll get 'xyz' is an invalid argument for cls).
        # the params have already been validated, you can still use
        # them in the view
        model_attributes = class_mapper(cls).attrs.keys()

        params = {
            k: v for k, v in params.items() if k in model_attributes
        }

        return cls(**params)
    end

    def update(self, params, force_save=True):
        for key in params:
            self.__setattr__(key, params[key])
        end

        return self.save() if force_save else self
    end

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self
    end

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self
    end

    def json(self):
        raise Exception(f"No json() function defined for class {self.__class__.__name__}")
    end
end
