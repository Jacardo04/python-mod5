from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    '''An abstract datastream base class'''
    def __init__(self, stream_id: str) -> None:
        '''creates a datastream processor'''
        self.stream_id = stream_id
        self.stats: Dict[str, Union[str, int, float]] = {}

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], 
                    criteria: Optional[str] = None) -> List[Any]:
        """ generic filter that just checks simpls stuff"""
        filtered = []
        for item in data_batch:
            if item is None:
                continue
            filtered.append(item)
        return filtered

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return self.stats


class SensorStream(DataStream):
    def __init__(self, stream_id):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        total = 0
        errors = 0
        count = 0
        self.stats['last_batch'] = data_batch

        for item in self.filter_data(data_batch):
            try:
                if isinstance(item, str) and ":" in item:
                    _, val = item.split(":")
                    value = float(val)
                else:
                    value = float(item)
                total += value
                count += 1
            except (ValueError, TypeError):
                errors += 1

        first_item = data_batch[0] if data_batch else 0
        if isinstance(first_item, str) and ":" in first_item:
            _, val = first_item.split(":")
            average = float(val)
        else:
            average = float(first_item)

        self.stats["count"] = count
        self.stats["errors"] = errors
        self.stats["average"] = average

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        filtered = super().filter_data(data_batch)
        result = []
        for item in filtered:
            if isinstance(item, (int, float)):
                result.append(item)
            elif isinstance(item, str) and ":" in item:
                result.append(item)
        return result

    def get_stats(self) -> str:
        return (
            "Initializing Sensor Stream...\n"
            f"Stream ID: {self.stream_id}, Type: Environmental Data\n"
            f"Processing sensor batch: {self.stats.get('last_batch', [])}\n"
            f"Sensor analysis: "
            f"{self.stats.get('count', 0)} readings processed, "
            f"avg temp: {self.stats.get('average', 0):.1f}°C\n"
        )


class TransactionStream(DataStream):
    def __init__(self, stream_id):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        errors = 0
        operations = 0
        net_flow = 0
        self.stats['last_batch'] = data_batch

        for item in self.filter_data(data_batch):
            try:
                op, val = item.split(":")
                value = int(val)
                if op == "buy":
                    net_flow += value
                elif op == "sell":
                    net_flow -= value
                operations += 1
            except (ValueError, TypeError, IndexError):
                errors += 1
        self.stats["errors"] = errors
        self.stats["net_flow"] = net_flow
        self.stats["count"] = operations

    def filter_data(self, data_batch: List[Any], criteria: Optional
                    [str] = None) -> List[Any]:
        """ first it filters from the generic made above"""
        filtered = super().filter_data(data_batch)
        """then we make a more specific filter"""
        result = []
        for item in filtered:
            if isinstance(item, str) and (item.startswith("buy:")
                                          or item.startswith("sell:")):
                # we append the item back to result
                result.append(item)
        return result

    def get_stats(self) -> str:
        return (
            "Initializing Transaction Stream...\n"
            f"Stream ID: {self.stream_id}, Type: Financial Data\n"
            f"Processing transaction batch: "
            f"{self.stats.get('last_batch', [])}\n"
            f"Transaction analysis: {self.stats.get('count', 0)} operations, "
            f"net flow: {self.stats.get('net_flow', 0):+} units\n"
            )


class EventStream(DataStream):
    def __init__(self, stream_id):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        errors = 0
        count = 0
        self.stats['last_batch'] = data_batch
        for item in self.filter_data(data_batch):
            count += 1
            # we use .lower here cause we need any instance where error is
            # written not just the prefix
            # .lower handles all ways to error could be written
            if "error" in item.lower():
                errors += 1
        self.stats["count"] = count
        self.stats["errors"] = errors

    def filter_data(self, data_batch: List[Any], criteria: Optional
                    [str] = None) -> List[Any]:
        """ first it filters from the generic made above"""
        filtered = super().filter_data(data_batch)
        result = []
        for item in filtered:
            if isinstance(item, str):
                result.append(item)
        return result

    def get_stats(self) -> str:
        return (
            "Initializing Event Stream...\n"
            f"Stream ID: {self.stream_id}, Type: System Events\n"
            f"Processing event batch: {self.stats.get('last_batch', [])}\n"
            f"Event analysis: {self.stats.get('count', 0)} events, "
            f"{self.stats.get('errors', 0)} error detected\n"
        )


class StreamProcessor:
    def __init__(self) -> None:
        self.streams = []

    def add_stream(self, stream: DataStream):
        self.streams.append(stream)

    def process_all(self, data_batches: Dict[str, list]):
        for stream in self.streams:
            batch = data_batches.get(stream.stream_id, [])
            stream.process_batch(batch)

    def show_all_stats(self):
        for stream in self.streams:
            print(stream.get_stats())


if __name__ == "__main__":
    processor = StreamProcessor()

    sensor = SensorStream("SENSOR_001")
    transaction = TransactionStream("TRANS_001")
    event = EventStream("EVENT_001")

    processor.add_stream(sensor)
    processor.add_stream(transaction)
    processor.add_stream(event)

    batches = {
        "SENSOR_001": ["temp:22.5", "humidity:65", "pressure:1013"],
        "TRANS_001": ["buy:100", "sell:150", "buy:75"],
        "EVENT_001": ["login", "error", "logout"]
    }

    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    processor.process_all(batches)
    processor.show_all_stats()
    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")
