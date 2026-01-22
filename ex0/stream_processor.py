from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):
    """ABSTRACT BASE CLASS"""
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        print("Initializing Numeric Processor...")

    def validate(self, data: Any) -> bool:
        print(f"Processing data: {data}")

        if not isinstance(data, list):
            return False
        is_valid: bool = all(isinstance(item, (int, float)) for item in data)

        if is_valid:
            print("Validation: Numeric data verified")

        return is_valid

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(f"Validation error: '{data}' is not numeric")
        total: float = sum(data)
        average: float = total / len(data)

        result: str = (
             f"Processed {len(data)} numeric values, "
             f"sum={total}, avg={average}"
        )

        return self.format_output(result)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        print("Initializing Text Processor...")

    def validate(self, data: Any) -> bool:
        print(f'Processing data: "{data}"')

        is_valid: bool = isinstance(data, str)

        if is_valid:
            print("Validation: Text data verified")

        return is_valid

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(
                f"Validation error: '{data}' is not valid text"
            )

        char_count: int = len(data)
        word_count: int = len(data.split())

        result: str = (
            f"Processed text: {char_count} characters, {word_count} words"
        )

        return self.format_output(result)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        print("Initializing Log Processor...")

    def validate(self, data: Any) -> bool:
        print(f'Processing data: "{data}"')
        is_valid: bool = isinstance(data, str) and ":" in data

        if is_valid:
            print("Validation: Log entry verified")
        return is_valid

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError(
                f"Validation error: '{data}' is not a valid log entry"
            )
        level, message = data.split(":", 1)
        level = level.strip()
        message = message.strip()

        result: str = f"[ALERT] {level} level detected: {message}"

        return self.format_output(result)


if __name__ == "__main__":
    print("\n--- EX0 POLYMORPHIC SELF TEST ---\n")

    # -----------------------
    # Factory method in the base class
    # -----------------------
    def get_processor_for_data(data: Any) -> DataProcessor:
        """Return the correct processor subclass for the given data."""
        if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            return NumericProcessor()
        elif isinstance(data, str) and ":" in data:
            return LogProcessor()
        elif isinstance(data, str):
            return TextProcessor()
        else:
            raise ValueError(f"No suitable processor for data: {data}")

    # -----------------------
    # Test data (valid + invalid)
    # -----------------------
    test_cases = [
        [1, 2, 3, 4, 5],                     # valid numeric
        "Hello Nexus World",                  # valid text
        "SUCCSESS: Connection established",          # valid log
        [1, 2, "three"],                      # invalid numeric
        12345,                                # invalid numeric
        12.5,                                 # invalid numeric
        123,                                  # invalid text
        "INVALID LOG ENTRY",                  # invalid log
    ]

    for data in test_cases:
        try:
            processor: DataProcessor = get_processor_for_data(data)
            print(processor.process(data))
        except Exception as e:
            print(f"Error processing {data!r}: {e}")
        print()  # empty line for readability