

class AbstractRepository:
    """ An Abstract repository. It consists of the funtionalities, the database specific Sub Classes need to have"""

    def __init__(self, repository_url: str):
        self.repo_url = repository_url

    @property
    def url(self) -> str:
        return self.repo_url

    def can_connect(self) -> bool:
        """Test the connection to the data store."""
        raise NotImplementedError("Repository.can_connect.")

    def initialize(self) -> bool:
        """Initialize the repository, if needed."""
        raise NotImplementedError("Repository.initialize.")


class Connection:  # pylint: disable=too-many-public-methods
    """Abstract connection to a reposity."""

    def close(self, success: bool) -> None:
        """Close the connection, store all permanent data."""
        raise NotImplementedError("Connection.close")


