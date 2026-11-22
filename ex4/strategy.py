from abc import ABC, abstractmethod

from ex3.capability import TransformCapability
from ex3.creature import Creature

from .errors import InvalidStrategyError


class BattleStrategy(ABC):
    """How a creature behaves during a battle."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Short name used for display."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Can this strategy be used by this creature?"""

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        """Make the creature act, return the messages produced."""


class NormalStrategy(BattleStrategy):
    @property
    def name(self) -> str:
        return "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    @property
    def name(self) -> str:
        return "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy")
        return [creature.transform(), creature.attack(), creature.revert()]
