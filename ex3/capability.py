from abc import ABC, abstractmethod


class TransformCapability(ABC):
    """An ability, NOT a creature: it does not inherit from Creature,
    so only the classes that choose it get transform/revert."""

    def __init__(self) -> None:
        self._transformed: bool = False

    @property
    def transformed(self) -> bool:
        return self._transformed

    @abstractmethod
    def transform(self) -> str:
        """Switch to the transformed state, return a message."""

    @abstractmethod
    def revert(self) -> str:
        """Go back to the normal state, return a message."""
