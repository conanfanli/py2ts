class UnknowFieldType(Exception):
    pass


class BadResolver(Exception):
    pass


class ValidationError(Exception):
    pass


class MissingField(ValidationError):
    pass
