#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Common interface shared by every data processor."""

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._storage: list[tuple[int, str]] = []
        self._total: int = 0

    @property #readonly and self every update
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


def test_numeric() -> None:
    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior "
          "validation:")
    try:
        numeric.ingest("foo") # mypy error expected here, because not validate in str
    except ValueError as error:
        print(f"Got exception: {error}")
    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    numeric.ingest(data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")


def test_text() -> None:
    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    data: list[str] = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data}")
    text.ingest(data)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")


def test_log() -> None:
    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    data: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {data}")
    log.ingest(data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print()
    test_numeric()
    print()
    test_text()
    print()
    test_log()
