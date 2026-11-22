#!/usr/bin/env python3

from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    fighter_1 = first.create_base()
    fighter_2 = second.create_base()
    print(fighter_1.describe())
    print(" vs.")
    print(fighter_2.describe())
    print(" fight!")
    print(fighter_1.attack())
    print(fighter_2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    test_factory(flame_factory)
    print()
    test_factory(transform_factory)
    print()
    test_battle(flame_factory, transform_factory)
