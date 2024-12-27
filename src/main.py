import sys

from Schedule import Schedule
from Parser import Parser
from State import State
from processControl import processControl

from pathlib import Path
import os

from orTree import or_tree_repair

MAX_GEN = 2000

# Access the debug environment variable
debug_mode = "False"
display_mode = "False"

def not_enough_slots(gs, ps):
    sum_g = 0
    sum_p = 0

    if debug_mode == "True": print("---Games---")
    for k, v in gs.items():
        max_g = max([slot.get_max() for slot in v]) # get the max of all games max for this time/DOW
        sum_g += max_g # accumulate sum of max game slots
    is_enough_gs = True if len(State.games) <= sum_g else False

    if debug_mode == "True": print("---Practices---")
    for k, v in ps.items():
        max_p = max([slot.get_max() for slot in v])
        sum_p += max_p
    is_enough_ps = True if len(State.practices) <= sum_p else False

    return is_enough_gs and is_enough_ps

def main():
    debug_mode = os.environ.get('DEBUG')
    display_mode = os.environ.get('DISPLAY')
    
    if debug_mode == None: debug_mode = "False"
    if display_mode == None: display_mode = "False"
    
    print("debug mode: ", debug_mode)
    print("display mode: ", display_mode)
    print("\n-----Running-----")
    
    filename = sys.argv[1]
    State.w_minfilled = int(sys.argv[2])
    State.w_pref = int(sys.argv[3])
    State.w_pair = int(sys.argv[4])
    State.w_secdiff = int(sys.argv[5])
    State.pen_gamemin = int(sys.argv[6])
    State.pen_practicemin = int(sys.argv[7])
    State.pen_notpaired = int(sys.argv[8])
    State.pen_section = int(sys.argv[9])

    if debug_mode == "True":
        print("filename: ", filename)
        print("WEIGHT AND PENALTY VALUES: ")
        print("w_minfilled: ", State.w_minfilled)
        print("w_pref: ", State.w_pref)
        print("w_pair: ", State.w_pair)
        print("w_secdiff: ", State.w_secdiff)
        print("pen_gamemin: ", State.pen_gamemin)
        print("pen_practicemin: ", State.pen_practicemin)
        print("pen_notpaired: ", State.pen_notpaired)
        print("pen_section: ", State.pen_section)
        print("\n")

    # Parsing the file
    if not filename.startswith("/Examples/") or not filename.startswith("../Examples/"):
        filename = "../Examples/" + filename            
    filepath = Path(filename)
    if not filepath.exists():
        raise Exception(f"Error: The file: '{filename}', does not exist.")
        
    Parser.parse_file(filename) # new

    if debug_mode == "True": 
        print("FINISHED PARSING")

    # Randomly generate 2 schedules
    schedule1 = Schedule(State.games, State.practices)
    schedule1.randomize_schedule()
    schedule1 = or_tree_repair(schedule1.get_assignments())

    schedule2 = Schedule(State.games, State.practices)
    schedule2.randomize_schedule()
    schedule2 = or_tree_repair(schedule2.get_assignments())

    # add schedules to population
    State.schedules.append(schedule1)
    State.schedules.append(schedule2)

    # check if we have enough slots to accommodate both practices and games
    is_enough_slots = not_enough_slots(State.game_slots, State.practice_slots)

    if is_enough_slots and schedule1 is not None and schedule2 is not None:
        for i in range(1, MAX_GEN):
            if display_mode == "True": print(f"--- GEN {i} ---")

            # Select which extension rule to apply
            processControl.f_wert(State.schedules)

            fit_values = State.f_fit(State.schedules)


            if display_mode == "True":
                print("===POPULATION===")
                for schedule, fitness in fit_values:
                    print(f"Schedule id: {schedule.get_id()} with fit value {fitness}")

            if State.fittest_schedule:
                is_fittest_in_pop = any(State.fittest_schedule == schedule for schedule, _ in fit_values)
                if not is_fittest_in_pop:
                    next_fittest = max(fit_values, key=lambda x: x[1])
                    State.fittest_schedule = next_fittest[0]
            
            if display_mode == "True": print("\n")

            # get the current fittest schedule in the population
            current_fittest, current_fittest_val = State.get_fittest(fit_values)
            
            if current_fittest_val > State.fittest_val:
                State.fittest_schedule = current_fittest
                State.fittest_val = current_fittest_val

            if display_mode == "True":
                print("CURRENT FITTEST VALUE:")
                print(f"Schedule {State.fittest_schedule.get_id()} with fit value {State.fittest_val}")
                print("\n")

    # print out the fittest schedule if it exists
    if State.fittest_schedule is not None:
        if display_mode == "True": print("\n\n--------\n\n")
        State.fittest_schedule.display_output()
        State.fittest_schedule.print_assignments()
    else:
        print("No schedule exists for this input file!")


if __name__ == "__main__":
    main()
