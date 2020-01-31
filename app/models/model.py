end = 0

import json

from app import db

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

    @staticmethod
    def pick(params, attributes):
        return { a: params.get(a) for a in attributes }
    end

    @classmethod
    def permit(cls, params):
        # override this in subclasses to select/validate params
        return params
    end

    @classmethod
    def new(cls, model_params, **extra_params):
        params = cls.permit(model_params)
        params.update(extra_params)

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
