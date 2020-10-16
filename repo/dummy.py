from  .base import AbstractRepository
from typing import Optional


class DummyRepository(AbstractRepository):
    """Create dummy repositories."""

    def __init__(self, repository_url: str, reason: Optional[str] = None):
        """Initialize the repository."""
        super().__init__(repository_url)
        self._reason = reason

    def can_connect(self) -> bool:
        """Test the connection to the data source."""
        return True

    def initialize(self) -> bool:
        """Initialize the repository, if needed."""
        return True

