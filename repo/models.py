""" Models for Repo Pattern not ORM. Objects are used to save the data loaded from the db not to save them like this"""
import dataclasses


@dataclasses.dataclass(frozen=True)  # pylint: disable=too-few-public-methods
class Model:
    """Base model for all model classes."""
    # frozen = True: The object is a read only instance. This is necessary, because data out of the db gets represented.


@dataclasses.dataclass(frozen=True)
class User(Model):
    key: str
    ident: str


