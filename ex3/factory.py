from abc import ABC, abstractmethod

from .creature import Creature
from .flame import Flameling, Pyrodon
from .shapeshifter import Morphagon, Shiftling


class CreatureFactory(ABC):
    """Abstract factory: a family of creatures (base + evolved)."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Create the base creature of the family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create the evolved creature of the family."""


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()
