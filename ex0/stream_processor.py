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
    print('=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n')

    print("VALID TESTS\n")

    try:
        numeric = NumericProcessor()
        print(numeric.process([1, 2, 3, 4, 5]))
    except Exception as e:
        print("Numeric error:", e)

    print()

    try:
        text = TextProcessor()
        print(text.process("Hello Nexus World"))
    except Exception as e:
        print("Text error:", e)

    print()

    try:
        log = LogProcessor()
        print(log.process("ERROR: Connection timeout"))
    except Exception as e:
        print("Log error:", e)

    print("\n INVALID TESTS\n")

    # Invalid numeric (contains text)
    try:
        bad_numeric = NumericProcessor()
        print(bad_numeric.process([1, 2, "three", 4]))
    except Exception as e:
        print("Numeric error:", e)

    print()

    # Invalid numeric (not a list)
    try:
        bad_numeric2 = NumericProcessor()
        print(bad_numeric2.process("12345"))
    except Exception as e:
        print("Numeric error:", e)

    print()

    # Invalid text (not a string)
    try:
        bad_text = TextProcessor()
        print(bad_text.process(12345))
    except Exception as e:
        print("Text error:", e)

    print()

    # Invalid log (missing colon)
    try:
        bad_log = LogProcessor()
        print(bad_log.process("ERROR Connection timeout"))
    except Exception as e:
        print("Log error:", e)