import random

from Game import Game
from Slot import Slot
from Practice import Practice

import sys
from pathlib import Path
import csv

class Schedule:
    """
    Represents a set of games and practices being assigned to a game or practice slot
    """

    id_count = 1

    def __init__(self, games: dict[str, Game], practices: dict[str, Practice]):
        self._assignment: dict[str, list[Slot]] = {}
        self._slot_assignment_counts: dict[str, int] = {} # stores the amount of times a slot has been assigned

        self._eval_value = 100
        self._fit_value = 100

        self._id = Schedule.id_count
        Schedule.id_count += 1
        
        # initializing an empty assignment for each game and practice
        for game in games.values():
            self._assignment[game.get_identifier()] = []
        for practice in practices.values():
            self._assignment[practice.get_identifier()] = []

        # Initializing counter at zero to track how many times a slot has been assigned
        from State import State
        for key in State.slots.keys():
            self._slot_assignment_counts[key] = 0

    def add_assign(self, field_identifier: str, slots: list[Slot]):
        if self._assignment[field_identifier] != slots:
            # check if field is already assigned to some slots
            if len(self._assignment[field_identifier]) != 0:
                # decrease the number of times the slots has been assigned
                for slot in self._assignment[field_identifier]:
                    self._slot_assignment_counts[slot.get_identifier()] -= 1

            # Assign field to new list of slots
            self._assignment[field_identifier] = slots
            for slot in slots:
                self._slot_assignment_counts[slot.get_identifier()] += 1

    def remove_assign(self, field_identifier: str):
        for slot in self._assignment[field_identifier]:
            self._slot_assignment_counts[slot.get_identifier()] -= 1

        self._assignment[field_identifier] = []

    def get_schedule(self):
        return self._assignment

    def get_assignment(self, field_identifier: str):
        return self._assignment[field_identifier]
    
    def get_assignments(self):
        """
        a helper function which returns the dictionary containing all of the slots in a schedule
        
        :param self: just schedule object that is calling this function
        :return: the dictionary containing all of the assignments
        """
        return self._assignment

    def get_id(self):
        return self._id

    def get_times_assigned(self, slot_identifier: str):
        return self._slot_assignment_counts[slot_identifier]

    def get_all_times_assigned(self):
        return self._slot_assignment_counts

    def clone_schedule(self, schedule: 'Schedule'):
        """
        clones the inputted schedule
        """
        for key, value in schedule.get_schedule().items():
            self._assignment[key] = value

        for key, value in schedule.get_all_times_assigned().items():
            self._slot_assignment_counts[key] = value

    def randomize_schedule(self):
        """Randomize all assignments in the schedule"""
        from State import State

        for identifier in self._assignment.keys():
            field = State.lookup_games_and_practices(identifier)
            if isinstance(field, Game):
                self.add_assign(identifier, random.choice(list(State.game_slots.values())))
            elif isinstance(field, Practice):
                self.add_assign(identifier, random.choice(list(State.practice_slots.values())))

    def randomize_assign(self):
        """Randomize one assignment (at random) in the schedule"""
        from State import State
        identifier = random.choice(list(self._assignment.keys()))
        field = State.lookup_games_and_practices(identifier)
        if isinstance(field, Game):
            self.add_assign(identifier, random.choice(list(State.game_slots.values())))
        elif isinstance(field, Practice):
            self.add_assign(identifier, random.choice(list(State.practice_slots.values())))

    def set_eval_value(self, value: int):
        self._eval_value = value

    def print_assignments(self):
        print(f"Eval-value: {self._eval_value}")
        for key, values in self._assignment.items():
            print(f"{key:<30}: ", end="")
            for slot in values:
                if slot is not None:
                    num_assigned = self.get_times_assigned(slot.get_identifier())
                    print(f"({slot.get_day()}, {slot.get_time()}), ", end="")
            print()
              
    # used mainly for the final output and names it based off input and is saved in Outputs dir             
    def display_output(self):
        file_name = Path(sys.argv[1]).stem
        output_dir = Path("../Outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{file_name}_displayed_schedule.csv"
        
        with open(output_file, mode="w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Division ", "Slot-Type ", "Weekday ", "Time ", "Number Assigned "])
            for division, values in self._assignment.items():
                for slot in values:
                    if slot is not None:
                        num_assigned = self.get_times_assigned(slot.get_identifier())
                        csv_writer.writerow([division, slot.slot_type, slot.day, slot.time, num_assigned])

    def __eq__(self, other):
        return self._assignment == other.get_schedule() and self._slot_assignment_counts == other.get_all_times_assigned()
