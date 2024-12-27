
from Schedule import Schedule
from Slot import Slot
from Game import Game

'''
computes penalty based on the minimum game/practice assignments to a slot
'''
def eval_minfilled(identifier, a: Schedule):
    from State import State
    penalty = 0
    gp_slot = list(State.slots.values())

    # calculate the penalty for each slot
    for slot in gp_slot:
        num_assigned = a.get_times_assigned(slot.get_identifier())
        min_value = slot.get_min()
        if slot.get_type() == 'g':
            if min_value - num_assigned > 0:
                penalty = penalty + State.pen_gamemin * (min_value - num_assigned)
        elif slot.get_type() == 'p':
            if min_value - num_assigned > 0:
                penalty = penalty + State.pen_practicemin * (min_value - num_assigned)

    return penalty

'''
Compares the current slots assigned to the identifier to its preffered slots. 
Returns a ranking point penalty if the current slot is not a preference slot
'''
def preference(identifier: str, a: Schedule) -> int:
    from State import State
    gp_assigned_slots = a.get_assignment(identifier)
    gp_pref = State.lookup_games_and_practices(identifier).get_preferences()
    penalty = 0

    for pref_val in gp_pref: # compare the game/practice being assigned to a slot
        pref_slot = pref_val[0]
        ranking_point = pref_val[1]
        if pref_slot not in gp_assigned_slots:
            penalty = penalty + ranking_point


    return penalty # if the assigned slot is contained within the list of preferences, then return 0

'''
returns pentaly if the identifier's assigned slots is not one of its preference
'''
def eval_pref(identifier: str, a: Schedule):
    penalty = preference(identifier, a=a)
    if penalty == 0:
        return 0
    else:
        return penalty

'''
helper function for eval_pair to determine if pairs have matching slots
'''
def pair(identifier: str, a: Schedule):
    from State import State
    penalty = 0
    field = State.lookup_games_and_practices(identifier)
    field_pair = field.get_pair()

    if field_pair and field.get_identifier():
        for pair in field_pair:
            pair_identifier = pair.get_identifier() # get identifier of pair
            base_list_slots = a.get_assignment(identifier) # get the list of slots of identifier
            pair_list_slots = a.get_assignment(pair_identifier) # get the list of slots of corresponding pair identifier
            index = 0
            for slot in base_list_slots: # compare the slot elements of each pair to see if they have the same slot
                if index < len(pair_list_slots):
                    pair_slot_day = pair_list_slots[index].get_day()
                    pair_slot_time = pair_list_slots[index].get_time()
                    if slot.get_day() != pair_slot_day or slot.get_time() != pair_slot_time:
                        penalty = penalty + State.pen_notpaired
                else: # for every number of slots missing in pair, add a penalty
                    penalty = penalty + State.pen_notpaired
                index += 1

    return penalty

'''
computes penalty if a, b in Games + Practices are not assigned to the same slot
'''
def eval_pair(identifier: str, a: Schedule):
    penalty = pair(identifier, a)
    return penalty


def multiple_div_slot(game_assign: Schedule, field):
    from State import State

    check_slots: list[Slot] = []
    tier = field.get_tier()
    for key, value in game_assign.get_schedule().items():
        current_field = State.lookup_games_and_practices(key)
        if tier in key and isinstance(current_field, Game) and field.get_id() != current_field.get_id():
            check_slots.extend(value)

    for slot in game_assign.get_assignment(field.get_identifier()):
        if slot in check_slots:
            return True

    return False

'''
returns a penatly if the times of divisional games within a single age/tier occur at the same time
'''
def eval_secdiff(identifier: str, a: Schedule):
    from State import State
    penalty = 0

    field = State.lookup_games_and_practices(identifier)
    is_diff_times = multiple_div_slot(a, field)

    if is_diff_times:
        penalty = State.pen_section
        return penalty
    return penalty


'''
computes the penalty based on eval soft constraints
'''
def eval(identifier, a: Schedule):
    from State import State

    evaluation = (
        eval_pref(identifier, a) * State.w_pref
        + (eval_pair(identifier, a) / 2) * State.w_pair
        + (eval_secdiff(identifier, a) / 2) * State.w_secdiff
    )
    return evaluation


'''
sums up all of the eval values for each assignment in a schedule
'''
def eval_sum(schedule: Schedule):
    from State import State

    eval_score = 0
    for k,_ in schedule.get_schedule().items():
        eval_score += eval(k, schedule)

    eval_score = eval_score + (eval_minfilled("test", schedule) * State.w_minfilled)
    return eval_score

