from .base import AbstractRepository
from .postgres import PostgresRepository
from .dummy import DummyRepository
from typing import Dict, Type


REPOSITORY_DIRECTORY: Dict[str, Type[AbstractRepository]] = {
    "postgres": PostgresRepository,
}


def url_parse(repo_url: str):
    """ parse the url. For now its just given that a : comes after the type of the url"""
    # example: postgres://user:pw@host/db_name  or something like that
    db_type = repo_url.split(':')[0]
    return db_type


def create_repository(repo_url: str) -> AbstractRepository:
    """Repository Factory"""
    if not repo_url:
        repository = DummyRepository(
            "dummy:", f"Repo url is not correct {repo_url}")
        return repository

    db_type = repo_url['type']
    try:
        repository = REPOSITORY_DIRECTORY[db_type](repo_url)
        # for postgres port, pw etc is needed so url should be a class or dict. Not only
    except KeyError:
        # If the URL doesnt fit any Key in REPOSITORY_DIRECTORY
        repository = DummyRepository(
            "dummy:", f"Unknown repository scheme '{db_type}'")

    # try if the db can connect. (Is postgres server running)
    if not repository.can_connect():
        repository = DummyRepository(
            "dummy:", f"Cannot connect to {repository.url}")

    # Check if the Schema exists, otherwise execute the schema
    if not repository.initialize():
        repository = DummyRepository(
            "dummy:", f"Cannot initialize repository {repository.url}")
    return repository
