end = 0

class ValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
    end
end

class Schema(object):
    def __init__(self, many=False):
        self.many = many
    end

    def validate_required(self, params, param, error):
        if not param in params:
            raise ValidationError(error)
        end
    end

    def load(self, params):
        return self.validate(params) if self.validate else params
    end

    def dump(self, model):
        if not self.many:
            return self.transform(model)
        end

        return [self.transform(m) for m in model]
    end
end
