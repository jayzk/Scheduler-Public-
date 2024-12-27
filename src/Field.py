"""
Games and Practices have a lot of attributes in common which is why there is a
parent class for both of them called Field. Both games and practices also have
non-compatible fields, unwanted time slots and preferences so these will be included here as
well.
"""

from abc import abstractmethod
from Slot import Slot

class Field:
    """
    Represents a generic field with attributes and behaviors common to both games and practices.
    Provides methods to manage non-compatible fields, unwanted slots, and time slot preferences.

    Attributes:
        id_count (int): A class-level counter to assign unique IDs to each field instance.
        league (str): The league to which the field belongs.
        tier (str): The tier of the league.
        div (str): The division of the field.
        _not_compatible (list[Field]): A list of fields that are not compatible with this field.
        _unwanted (list[Slot]): A list of unwanted timeslots for this field.
        _preferences (list[tuple[Slot, int]]): A list of preferred time slots with corresponding preference values.
        _pair (Field | None): Another field paired with this one.
        _partial_assign (Slot | None): A partially assigned time slot for this field.
        _id (int): A unique identifier for the field instance.
    """

    id_count = 1

    def __init__(self, league: str, tier: str, div: str):
        self.league = league
        self.tier = tier
        self.div = div

        self._not_compatible: list[Field] = [] # list of non-compatible fields
        self._unwanted: list[Slot] = [] # list of unwanted slots
        self._preferences: list[tuple[Slot, int]] = [] # list of preferences (Slot, preference value)
        self._pair: list[Field] = [] # Paired field
        self._partial_assign: Slot = None # Partially assigned slot

        self._id = Field.id_count
        Field.id_count += 1

    # Getter methods
    def get_league(self):
        """Returns the league of the field."""
        return self.league

    def get_tier(self):
        """Returns the tier of the field."""
        return self.tier

    def get_div(self):
        """Returns the division of the field."""
        return self.div

    def get_not_compatible(self):
        """Returns the list of non-compatible fields."""
        return self._not_compatible

    def get_unwanted(self):
        """Returns the list of unwanted time slots."""
        return self._unwanted

    def get_preferences(self):
        """Returns the list of preferred time slots and their preference values."""
        return self._preferences

    def get_pair(self):
        """Returns the paired field, if any."""
        # if self._pair is not None:
        #     return self._pair
        return self._pair

    def get_partial_assign(self):
        """Returns the partially assigned time slot, if any."""
        if self._partial_assign is not None:
            return self._partial_assign

    def get_id(self):
        """Returns the unique ID of the field."""
        return self._id

    # Methods for managing non-compatible fields
    def add_not_compatible(self, field: 'Field'):
        """
        Adds a field to the non-compatible list.

        Args:
            field (Field): The field to mark as non-compatible.
        """
        self._not_compatible.append(field)

    def remove_not_compatible(self, field: 'Field'):
        """
        Removes a field from the non-compatible list.

        Args:
            field (Field): The field to remove from the non-compatible list.
        """
        self._not_compatible.remove(field)

    # Methods for managing unwanted slots
    def add_unwanted(self, slot: Slot):
        """
        Adds a time slot to the unwanted list.

        Args:
            slot (Slot): The slot to mark as unwanted.
        """
        self._unwanted.append(slot)

    def remove_unwanted(self, slot: Slot):
        """
        Removes a time slot from the unwanted list.

        Args:
            slot (Slot): The slot to remove from the unwanted list.
        """
        self._unwanted.remove(slot)

    # Methods for managing preferences
    def add_preferences(self, slot: Slot, value: int):
        """
        Adds a preferred time slot with its priority value.

        Args:
            slot (Slot): The preferred time slot.
            value (int): The priority value for the slot.
        """
        self._preferences.append((slot, value))

    # Methods for managing paired fields
    def add_pair(self, field: 'Field'):
        """
        Sets another field as paired with this one.

        Args:
            field (Field): The field to pair with.
        """
        # self._pair = field
        self._pair.append(field)

    # Methods for managing partial assignments
    def add_partial_assign(self, slot: Slot):
        """
        Sets a time slot as partially assigned to this field.

        Args:
            slot (Slot): The slot to partially assign.
        """
        self._partial_assign = slot

    # Debugging and information methods
    def get_identifying_info(self):
        """
        Returns a string containing identifying information for the field.
        """
        return (
            f"{self.league}, {self.tier}, div {self.div}"
        )

    def print_unwanted(self):
        """
        Prints all unwanted time slots for the field.
        """
        for slot in self._unwanted:
            print(f"-  {slot.get_all_info()}")

    def print_not_compatible(self):
        """
        Prints all non-compatible fields for the field.
        """
        for field in self._not_compatible:
            print(f"-  {field.get_identifier()}")

    def print_preferences(self):
        """
        Prints all preferred time slots and their priorities for the field.
        """
        for preference in self._preferences:
            print(f"-  ({preference[0].get_all_info()}), {preference[1]}")

    @abstractmethod
    def get_identifier(self):
        """Abstract method to return a unique identifier for the field."""
        pass

    @abstractmethod
    def print_info(self):
        """Abstract method to print all information about the field."""
        pass