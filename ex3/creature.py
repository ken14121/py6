from abc import ABC, abstractmethod


class Creature(ABC):
    """Base of every entity: a name, a type, an attack."""

    def __init__(self, name: str, creature_type: str) -> None:
        self._name: str = name
        self._type: str = creature_type

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def attack(self) -> str:
        """Return the attack message of this creature."""

    def describe(self) -> str:
        return f"{self._name} is a {self._type} type Creature"
