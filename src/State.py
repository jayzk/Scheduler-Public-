from datetime import datetime
from typing import Tuple

from Game import Game
from Practice import Practice
from Slot import Slot
from Schedule import Schedule
from Datatypes.Day import Day
from Datatypes.SlotType import SlotType
from eval import eval_sum
from Schedule import Schedule



class State:
    """
    A centralized data storage and retrieval class for managing slots, games, and practices

    Attributes:
    slots : dict[str, Slot]
        A dictionary that stores slots where:
        - Key: A string in the format "slot_type, day, time".
        - Value: A Slot object representing the corresponding time slot.

    game_slots : dict[tuple[tuple[str], datetime.time], list[Slot]]
        Represents the simplified game slots
        A dictionary that maps combined days and times to a list of Slot objects for games.
        - Key: A tuple of the form ((day1, day2, ...), time).
        - Value: A list of Slot objects.

    practice_slots : dict[tuple[tuple[str], datetime.time], list[Slot]]
        Represents the simplified practice slots
        A dictionary that maps combined days and times to a list of Slot objects for practices.
        - Key: A tuple of the form ((day1, day2, ...), time).
        - Value: A list of Slot objects.

    games : dict[str, Game]
        A dictionary that stores games where:
        - Key: A string identifier for the game.
        - Value: A Game object.

    practices : dict[str, Practice]
        A dictionary that stores practices where:
        - Key: A string identifier for the practice.
        - Value: A Practice object.
        
    assignments: list[Assignment]
        A list that stores assignments (our facts)
    """

    slots: dict[str, Slot] = {} # slots contains the non-simplified version of our time slots
    game_slots: dict[str, list[Slot]] = {}  # game_slots contains our simplified game slots
    practice_slots: dict[str, list[Slot]] = {}  # practice_slots contains our simplified practice slots


    games: dict[str, Game] = {} # games contains our list of games
    practices: dict[str, Practice] = {} # practices contains our list of practices

    schedules: list[Schedule] = [] # list of assignments/schedules/facts

    fittest_schedule: Schedule = None # initial as None
    fittest_val: int = 0

    is_schedule_possible = True

    # penalty and weight values
    w_minfilled: int
    w_pref: int
    w_pair: int
    w_secdiff: int
    pen_gamemin: int
    pen_practicemin: int
    pen_notpaired: int
    pen_section: int

    # config vars (may change alot)
    max_pop_size = 10
    max_fit = 100000

    @staticmethod
    def lookup_slots(slot_type: str, day: str, time: datetime.time):
        # check if slot exists
        key = f"{slot_type}, {day}, {time}"
        if key in State.slots:
            return State.slots[key]
        else:
            raise Exception(f"Key ({key}) not found in slots!")

    @staticmethod
    def lookup_games_and_practices(identifier: str):
        # check if it is a game
        if identifier in State.games:
            return State.games[identifier]
        elif identifier in State.practices: # check if it is a practice
            return State.practices[identifier]
        else:
            raise Exception(f"{identifier} not found in games or practices!")

    @staticmethod
    def lookup_simple_slots(type: str, day: str, time: datetime.time):
        if type == SlotType.GAME:
            if day == Day.MONDAY or day == Day.WEDNESDAY or day == Day.FRIDAY:
                key = f"MWF, {time}"
                return State.game_slots[key]
            elif day == Day.TUESDAY or day == Day.THURSDAY:
                key = f"TTh, {time}"
                return State.game_slots[key]
        if type == SlotType.PRACTICE:
            if day == Day.MONDAY or day == Day.WEDNESDAY:
                key = f"MW, {time}"
                return State.practice_slots[key]
            elif day == Day.TUESDAY or day == Day.THURSDAY:
                key = f"TTh, {time}"
                return State.practice_slots[key]
            elif day == Day.FRIDAY:
                key = f"F, {time}"
                return State.practice_slots[key]

    @staticmethod
    def check_duplicate_schedules(schedule: Schedule):
        from orTree import or_tree_repair

        """Try to prevent inputted schedule from being a duplicate"""
        for i in range(1, 10):  # Give it a max of 10 tries
            if schedule in State.schedules:  # new_schedule1 is a duplicate
                schedule.randomize_assign()

                schedule = or_tree_repair(schedule.get_assignments())

                if schedule is None:
                    State.is_schedule_possible = False
                    break
            else:
                break
       
    #f_fit functions:      
    @staticmethod
    def f_fit(schedules: list[Schedule]) -> list[tuple[Schedule, int]]: # pass in state.schedules i.e F
        fit_values = []

        for schedule in schedules:
            schedule_eval = eval_sum(schedule)
            schedule.set_eval_value(schedule_eval)
            fit_values.append((schedule, State.max_fit - schedule_eval))

        return fit_values # list of tuples (name, fit value)
    
    # add tie breaking 
    @staticmethod
    def lookup_simple_slot(type: str):
        """
        This is a helper function which returns all of the slots for a given game type, so either games or practice
        
        :param type: this will either be SlotType.GAME or SlotType.Practice depending on which game type you want to return
        :return: either returns a dictioanry of all slots corresping to games or all slots corresping to games
        """
        
        # check to see if we want to return game slots
        if type == SlotType.GAME:
            # if that is the case then return all the game slots
            return State.game_slots
        # check to otherwise see if we want to return all practice slots
        if type == SlotType.PRACTICE:
            # if that is the case then return all practice slots
            return State.practice_slots

    @staticmethod
    def f_unfit(fit_set: list[tuple[Schedule, int]]):
        sorted_fits = sorted(fit_set, key=lambda x: x[1])
        return sorted_fits[0][0], sorted_fits[1][0]
    
    @staticmethod
    def f_findFittest(fit_set: list[tuple[Schedule, int]]):
        sorted_fits = sorted(fit_set, key=lambda x: x[1], reverse=True)
        return sorted_fits[0][0], sorted_fits[1][0]

    @staticmethod
    def lookup_games_by_tier(tier: str):
        games_list = []
        for identifier in State.games:
            if tier in identifier:
                games_list.append(State.games[identifier])
        return games_list

    @staticmethod
    def get_fittest(fit_set: list[tuple[Schedule, int]]) -> tuple[Schedule, int]: 
        sorted_fits = sorted(fit_set, key=lambda x: x[1], reverse=True)
        return sorted_fits[0]

    @staticmethod
    def clear():
        State.slots.clear()
        State.game_slots.clear()
        State.practice_slots.clear()
        State.games.clear()
        State.practices.clear()
        State.schedules.clear()

        State.w_minfilled = 0
        State.w_pref = 0
        State.w_pair = 0
        State.w_secdiff = 0
        State.pen_gamemin = 0
        State.pen_practicemin = 0
        State.pen_notpaired = 0
        State.pen_section = 0
