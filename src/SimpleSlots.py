
from Datatypes.Day import Day
from Datatypes.SlotType import SlotType
from Slot import Slot
from State import State


class SimpleSlots:
    """
    This class is mostly used to convert regular time slots to our simplified
    time slots of game slots and practice slots.
    """
    @staticmethod
    def add_simple_slot(slot: Slot):
        # Get the corresponding combined day
        combined_day = None
        if slot.slot_type == SlotType.GAME:
            if slot.day == Day.MONDAY or slot.day == Day.WEDNESDAY or slot.day == Day.FRIDAY:
                combined_day = "MWF"
            elif slot.day == Day.TUESDAY or slot.day == Day.THURSDAY:
                combined_day = "TTh"
        elif slot.slot_type == SlotType.PRACTICE:
            if slot.day == Day.MONDAY or slot.day == Day.WEDNESDAY:
                combined_day = "MW"
            elif slot.day == Day.TUESDAY or slot.day == Day.THURSDAY:
                combined_day = "TTh"
            elif slot.day == Day.FRIDAY:
                combined_day = "F"

        # create key for the dictionary
        key = f"{combined_day}, {slot.get_time()}"

        if slot.slot_type == SlotType.GAME: # If the time slot is for games
            # If the key does not yet exist create an empty list for the value
            if key not in State.game_slots:
                State.game_slots[key] = []
            State.game_slots[key].append(slot)
        elif slot.slot_type == SlotType.PRACTICE: # If the time slot is for practices
            # If the key does not yet exist create an empty list for the value
            if key not in State.practice_slots:
                State.practice_slots[key] = []
            State.practice_slots[key].append(slot)

    @staticmethod
    def simplify_slots(slots: dict[str, Slot]):
        for slot in slots.values():
            SimpleSlots.add_simple_slot(slot)