from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.logging import log
from surmount.data import NDWFirstTrustFocusFive, NDWFirstTrustFocusFiveTrades
from datetime import datetime


def run(self, data):
    for i in self.data_list:
        key = tuple(i)
        print("Available data keys:", data.keys())
        print("Checking key:", key)

        if key[0] == "ndw_ftrust5":
            ndw_data = data.get(key)
            print("NDW DATA:", ndw_data)

            if not ndw_data:
                print("No NDW data found")
                return None

            allocations = ndw_data[-1].get("allocations", {})
            print("ALLOCATIONS:", allocations)

            total = sum(allocations.values())
            print("TOTAL:", total)

            if total > 0:
                normalized = {k: v / total for k, v in allocations.items()}
                print("RETURNING:", normalized)
                return TargetAllocation(normalized)

    print("Returning None at end")
    return None