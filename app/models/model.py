end = 0

import json

from app import db

from sqlalchemy.orm import class_mapper

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
    def get(cls, id):
        return cls.query.get(id)
    end

    @classmethod
    def one(cls, **params):
        return cls.all(**params).first()
    end

    @classmethod
    def new(cls, **params):
        if not cls.__name__ in schemas:
            raise Exception(f"No schema is defined for class {cls.__name__}")
        end

        model_params = schemas[cls.__name__].load(params)

        # filter out the params that are not part of the class model
        # (otherwise you'll get 'xyz' is an invalid argument for cls).
        # the params have already been validated, you can still use
        # them in the view
        model_attributes = class_mapper(cls).attrs.keys()

        model_params = {
            k: v for k, v in model_params.items() if k in model_attributes
        }

        # add the new object to the session so that when dependent
        # objects are similarly created, they, too, are added to
        # the same session so they can be committed together. if
        # this is not done, then saving one object might result in
        # an error because a dependent object hasn't been saved yet
        new_object = cls(**model_params)

        db.session.add(new_object)

        return new_object
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
end
