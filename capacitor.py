#!/usr/bin/env python3

from ex3 import TransformCreatureFactory


if __name__ == "__main__":
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()
    for label, creature in (("base", base), ("evolved", evolved)):
        print()
        print(f" {label}:")
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
