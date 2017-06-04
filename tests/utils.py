from schematics.models import Model
from schematics.types import IntType


class User(Model):
    points = IntType()
