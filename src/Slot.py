from Datatypes.Day import Day
from datetime import datetime
from Datatypes.SlotType import SlotType

class Slot:
    """
    Represents a non-simplified time slot.

    The `Slot` class encapsulates information about a specific time slot, including the type of the slot
    (e.g., lecture, lab), the day it occurs, the time of the slot, and its maximum and minimum values.
    Each `Slot` instance also has a unique identifier and an auto-incremented ID.

    Attributes:
            slot_type (SlotType): The type of the slot (g or p).
            day (Day): The day of the week the slot occurs.
            time (datetime.time): The time at which the slot starts.
            max (int): The maximum capacity for the slot.
            min (int): The preferred minimum capacity for the slot.
    """

    # Note: we don't really use this, just here just in case
    id_count = 1

    def __init__(self, slot_type: SlotType, day: Day, time: datetime.time, max: int, min: int):
        self.slot_type = slot_type
        self.day = day
        self.time = time
        self.max = max
        self.min = min

        self._id = Slot.id_count
        self._identifier = f"{slot_type}, {day}, {time}"
        Slot.id_count += 1

    def print_slot(self):
        """
        Prints all relevant information about the slot, including:
        - Slot ID, identifier, type, day, time, max capacity, and min capacity.
        """

        print("---SLOT INFO---")
        print("ID: ", self._id)
        print("Identifier: ", self._identifier)
        print("Type: ", self.slot_type)
        print("Day: ", self.day)
        print("Time: ", self.time)
        print("Max: ", self.max)
        print("Min: ", self.min)
        print("---------------")

    # get methods
    def get_type(self):
        """Returns the type of the slot."""
        return self.slot_type

    def get_day(self):
        """Returns the day of the week the slot occurs."""
        return self.day

    def get_time(self):
        """Returns the time at which the slot starts."""
        return self.time

    def get_max(self):
        """Returns the maximum capacity for the slot."""
        return self.max

    def get_min(self):
        """Returns the minimum capacity for the slot."""
        return self.min

    def get_id(self):
        """Returns the unique ID of the slot."""
        return self._id

    def get_identifier(self):
        """Returns the unique identifier of the slot."""
        return self._identifier

    # Mostly used for debugging
    def get_all_info(self):
        """Returns a formatted string containing all the information about the slot."""
        return (
            f"{self.slot_type}, {self.day}, {self.time}, "
            f"{str(self.max)}, {str(self.min)}"
        )

    def __eq__(self, other):
        return self._identifier == other.get_identifier()