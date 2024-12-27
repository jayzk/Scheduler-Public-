from datetime import datetime

from Datatypes.SlotType import SlotType
from Field import Field
from Game import Game
from Practice import Practice
from SimpleSlots import SimpleSlots
from Slot import Slot
from State import State

# Constants
GAME_SLOTS = 0
PRACTICE_SLOTS = 1
GAMES = 2
PRACTICES = 3
NOT_COMPATIBLE = 4
UNWANTED = 5
PREFERENCES = 6
PAIR = 7
PARTIAL_ASSIGN = 8

class Parser:
    @staticmethod
    def parse_file(file_name: str):
        # keeps track of what we are currently parsing
        currently_parsing = -1

        # keeps track of what sections we need to parse
        parsed_sections = ["Game slots:", "Practice slots:", "Games:", "Practices:", "Not compatible:",
                           "Unwanted:", "Preferences:", "Pair:", "Partial assignments:"]

        # open the file for reading
        f = open(file_name, "r")

        # iterate through each line in the file
        for line in f:
            # strip the line of any excess whitespace or newline chars
            line = line.strip()

            # check what we are currently parsing
            if line == parsed_sections[GAME_SLOTS]:
                currently_parsing = GAME_SLOTS
            elif line  == parsed_sections[PRACTICE_SLOTS]:
                currently_parsing = PRACTICE_SLOTS
            elif line  == parsed_sections[GAMES]:
                currently_parsing = GAMES

                # at this point all time slots have been stored and can be simplified
                SimpleSlots.simplify_slots(State.slots)
            elif line  == parsed_sections[PRACTICES]:
                currently_parsing = PRACTICES
            elif line  == parsed_sections[NOT_COMPATIBLE]:
                currently_parsing = NOT_COMPATIBLE
            elif line  == parsed_sections[UNWANTED]:
                currently_parsing = UNWANTED
            elif line  == parsed_sections[PREFERENCES]:
                currently_parsing = PREFERENCES
            elif line  == parsed_sections[PAIR]:
                currently_parsing = PAIR
            elif line  == parsed_sections[PARTIAL_ASSIGN]:
                currently_parsing = PARTIAL_ASSIGN

            # skip any blank lines or any line that contains the parsed_sections
            if line == "" or line in parsed_sections:
                continue

            # store info
            if currently_parsing == GAME_SLOTS:
                parse_slots(line, SlotType.GAME)
            elif currently_parsing == PRACTICE_SLOTS:
                parse_slots(line, SlotType.PRACTICE)
            elif currently_parsing == GAMES:
                parse_games(line)
            elif currently_parsing == PRACTICES:
                parse_practices(line)
            elif currently_parsing == NOT_COMPATIBLE:
                parse_not_compatible(line)
            elif currently_parsing == UNWANTED:
                parse_unwanted(line)
            elif currently_parsing == PREFERENCES:
                parse_preferences(line)
            elif currently_parsing == PAIR:
                parse_pair(line)
            elif currently_parsing == PARTIAL_ASSIGN:
                parse_partial_assign(line)

        # close the file
        f.close()

# Helper functions
def parse_slots(line: str, slot_type: SlotType):
    result = [item.strip() for item in line.split(",")]

    # parse information
    day = result[0]
    time = datetime.strptime(result[1], '%H:%M').time()
    max = int(result[2])
    min = int(result[3])
    slot = Slot(slot_type, day, time, max, min)

    # store information
    State.slots[slot.get_identifier()] = slot


def parse_games(line: str):
    result = [item.strip() for item in line.split(" ")]

    league = result[0]
    tier = result[1]
    div = result[3]

    # consider special games
    if league == "CMSA" and tier == "U12T1":
        practice = Practice(league, tier+'S', "01", "PRC", "01")
        if practice not in list(State.practices.values()):
            State.practices[practice.get_identifier()] = practice
    elif league == "CMSA" and tier == "U13T1":
        practice = Practice(league, tier+'S', "01", "PRC", "01")
        if practice not in list(State.practices.values()):
            State.practices[practice.get_identifier()] = practice

    game = Game(league, tier, div)
    State.games[game.get_identifier()] = game

def parse_practices(line: str):
    result = [item.strip() for item in line.split(" ")]

    league = result[0]
    tier = result[1]
    div = "0"

    practice_num = 0
    practice_type = None

    if result[2] == "DIV":
        div = result[3]
        practice_type = result[4]
        practice_num = result[5]
    elif result[2] == "PRC" or result[2] == "OPN":
        practice_type = result[2]
        practice_num = result[3]
    practice = Practice(league, tier, div, practice_type, practice_num)
    State.practices[practice.get_identifier()] = practice

def parse_not_compatible(line: str):
    result = [item.strip() for item in line.split(",")]

    first_field: Field = None
    second_field: Field = None

    if result[0] in State.games:
        first_field = State.games[result[0]]
    elif result[0] in State.practices:
        first_field = State.practices[result[0]]

    if result[1] in State.games:
        second_field = State.games[result[1]]
    elif result[1] in State.practices:
        second_field = State.practices[result[1]]

    first_field.add_not_compatible(second_field)
    second_field.add_not_compatible(first_field)

def parse_unwanted(line: str):
    result = [item.strip() for item in line.split(",")]

    identifier = result[0]
    day = result[1]
    time = datetime.strptime(result[2], '%H:%M').time()

    if identifier in State.games:
        game = State.games[identifier]
        key = f"g, {day}, {time}"
        slot = State.slots[key]
        game.add_unwanted(slot)
    elif identifier in State.practices:
        practice = State.practices[identifier]
        key = f"p, {day}, {time}"
        slot = State.slots[key]
        practice.add_unwanted(slot)

def parse_preferences(line: str):
    result = [item.strip() for item in line.split(",")]

    day = result[0]
    time = datetime.strptime(result[1], '%H:%M').time()
    slot = None
    field = State.lookup_games_and_practices(result[2])
    value = int(result[3])

    if isinstance(field, Game):
        slot = State.lookup_slots(SlotType.GAME, day, time)
    elif isinstance(field, Practice):
        slot = State.lookup_slots(SlotType.PRACTICE, day, time)
    else:
        raise Exception("Invalid field!")

    field.add_preferences(slot, value)

def parse_pair(line: str):
    result = [item.strip() for item in line.split(",")]

    first_field = State.lookup_games_and_practices(result[0])
    second_field = State.lookup_games_and_practices(result[1])
    first_field.add_pair(second_field)
    second_field.add_pair(first_field)

def parse_partial_assign(line: str):
    result = [item.strip() for item in line.split(",")]

    field = State.lookup_games_and_practices(result[0])
    day = result[1]
    time = datetime.strptime(result[2], '%H:%M').time()

    if isinstance(field, Game):
        slot = State.lookup_slots(SlotType.GAME, day, time)
    elif isinstance(field, Practice):
        slot = State.lookup_slots(SlotType.PRACTICE, day, time)
    else:
        raise Exception("Invalid field!")

    field.add_partial_assign(slot)