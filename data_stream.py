#!/usr/bin/env python3

import typing
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Common interface shared by every data processor."""

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._storage: list[tuple[int, str]] = []
        self._total: int = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def total(self) -> int:
        """Number of items ingested since creation."""
        return self._total

    @property
    def remaining(self) -> int:
        """Number of items still waiting to be extracted."""
        return len(self._storage)

    def _store(self, value: str) -> None:
        """Helper used by every subclass: give the item its rank."""
        self._storage.append((self._total, value))
        self._total += 1

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Return True if this processor can ingest data."""

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Store data, raise ValueError if it is not appropriate."""

    def output(self) -> tuple[int, str]:
        """Remove and return the oldest item with its rank (FIFO)."""
        if not self._storage:
            raise IndexError(f"{self._name}: no data left")
        return self._storage.pop(0)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if is_number(data):
            return True
        return (isinstance(data, list) and len(data) > 0
                and all(is_number(item) for item in data))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return (isinstance(data, list) and len(data) > 0
                and all(isinstance(item, str) for item in data))

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


def is_log(value: Any) -> bool:
    return isinstance(value, dict) and len(value) > 0 and all(
        isinstance(k, str) and isinstance(v, str) for k, v in value.items()
    )


def log_to_str(log: dict[str, str]) -> str:
    if "log_level" in log and "log_message" in log:
        return f"{log['log_level']}: {log['log_message']}"
    return ", ".join(f"{key}: {value}" for key, value in log.items())


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    def validate(self, data: Any) -> bool:
        if is_log(data):
            return True
        return (isinstance(data, list) and len(data) > 0
                and all(is_log(item) for item in data))

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._store(log_to_str(item))
        else:
            self._store(log_to_str(data))


class DataStream:
    """Routes each element of a stream to the first processor that
    accepts it. It only knows the DataProcessor interface."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    try:
                        proc.ingest(element)
                    except ValueError as error:
                        print(f"DataStream error - {error}")
                    break
            else:
                print("DataStream error - Can't process element in "
                      f"stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        for proc in self._processors:
            print(f"{proc.name}: total {proc.total} items processed, "
                  f"remaining {proc.remaining} on processor")


BATCH: list[typing.Any] = [
    "Hello world",
    [3.14, -1, 2.71],
    [{"log_level": "WARNING",
      "log_message": "Telnet access! Use ssh instead"},
     {"log_level": "INFO", "log_message": "User wil is connected"}],
    42,
    ["Hi", "five"],
]


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    print()
    print("Registering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    print()
    print(f"Send first batch of data on stream: {BATCH}")
    stream.process_stream(BATCH)
    stream.print_processors_stats()
    print()
    print("Registering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(BATCH)
    stream.print_processors_stats()
    print()
    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for proc, count in ((numeric, 3), (text, 2), (log, 1)):
        for _ in range(count):
            proc.output()
    stream.print_processors_stats()
