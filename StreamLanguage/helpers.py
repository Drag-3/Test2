import models


def type_check(a: models.Type, b: models.Type):
    if a.name == b.name:
        return True
    else:
        return False

def type_toPython(a: models.Type):
    if a.name == "int":
        return int
    elif a.name == "string":
        return str
    elif a.name == "bool":
        return bool
    else:
        return None

def type_fromPython(a):
    if type(a) == int:
        return models.IntType()
    elif type(a) == str:
        return models.StringType()
    elif type(a) == bool:
        return models.BoolType()
    else:
        return models.UndefinedType()