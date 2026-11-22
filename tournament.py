#!/usr/bin/env python3

from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (AggressiveStrategy, BattleStrategy, InvalidStrategyError,
                 NormalStrategy)

Opponent = tuple[CreatureFactory, BattleStrategy]


def fight(first: Opponent, second: Opponent) -> None:
    creature_1 = first[0].create_base()
    creature_2 = second[0].create_base()
    print("* Battle *")
    print(creature_1.describe())
    print(" vs.")
    print(creature_2.describe())
    print(" now fight!")
    for creature, strategy in ((creature_1, first[1]),
                               (creature_2, second[1])):
        for message in strategy.act(creature):
            print(message)


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                fight(opponents[i], opponents[j])
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def show_line_up(title: str, opponents: list[Opponent]) -> None:
    print(title)
    labels: list[str] = [
        f"({factory.create_base().name}+{strategy.name})"
        for factory, strategy in opponents
    ]
    print("[ " + ", ".join(labels) + " ]")


if __name__ == "__main__":
    flame = FlameFactory()
    shift = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    tournaments: list[tuple[str, list[Opponent]]] = [
        ("Tournament 0 (basic)", [(flame, normal), (shift, aggressive)]),
        ("Tournament 1 (error)", [(shift, aggressive), (flame, aggressive)]),
        ("Tournament 2 (multiple)",
         [(flame, normal), (shift, aggressive), (shift, normal)]),
    ]
    for title, opponents in tournaments:
        show_line_up(title, opponents)
        battle(opponents)
        print()
