import random

from Schedule import Schedule
from State import State
from Game import Game
from Practice import Practice
from orTree import or_tree_repair


class Extensions:
    @staticmethod
    def mutation(a: Schedule, b: Schedule):
        new_schedule1 = Extensions.random_assign(a)
        new_schedule2 = Extensions.random_assign(b)

        new_schedule1 = or_tree_repair(new_schedule1.get_assignments())
        new_schedule2 = or_tree_repair(new_schedule2.get_assignments())

        if new_schedule1 is not None and new_schedule2 is not None:
            # Try to prevent new_schedule1 being a duplicate
            State.check_duplicate_schedules(new_schedule1)

            # Try to prevent new_schedule2 being a duplicate
            State.check_duplicate_schedules(new_schedule2)
            
            new_schedule1 = or_tree_repair(new_schedule1.get_assignments())
            new_schedule2 = or_tree_repair(new_schedule2.get_assignments())

            # Add new schedules
            State.schedules.append(new_schedule1)
            State.schedules.append(new_schedule2)
        else:
            State.is_schedule_possible = False

    @staticmethod
    def crossover(a: Schedule, b: Schedule):
        num_games = len(State.games)
        num_practices = len(State.practices)

        j = -1
        if num_practices != 0:
            j = random.randint(1, num_practices) # for practices

        i = -1
        if num_games != 0:
            i = random.randint(1, num_games) # for games
        
        new_schedule1 = Schedule(State.games, State.practices)
        new_schedule2 = Schedule(State.games, State.practices)

        new_schedule1.clone_schedule(a)
        new_schedule2.clone_schedule(b)

        # Do crossover on the set of games
        if i != -1:
            count = 0
            for identifier in State.games.keys():
                if count >= i:
                    temp1 = new_schedule1.get_assignment(identifier)
                    temp2 = new_schedule2.get_assignment(identifier)
                    new_schedule1.add_assign(identifier, temp2)
                    new_schedule2.add_assign(identifier, temp1)
                count += 1

        if j != -1:
            count = 0
            for identifier in State.practices.keys():
                if count >= j:
                    temp1 = new_schedule1.get_assignment(identifier)
                    temp2 = new_schedule2.get_assignment(identifier)
                    new_schedule1.add_assign(identifier, temp2)
                    new_schedule2.add_assign(identifier, temp1)
                count += 1

        new_schedule1 = or_tree_repair(new_schedule1.get_assignments())
        new_schedule2 = or_tree_repair(new_schedule2.get_assignments())


        # Try to prevent new_schedule1 being a duplicate
        State.check_duplicate_schedules(new_schedule1)

        # Try to prevent new_schedule2 being a duplicate
        State.check_duplicate_schedules(new_schedule2)
        
        new_schedule1 = or_tree_repair(new_schedule1.get_assignments())
        new_schedule2 = or_tree_repair(new_schedule2.get_assignments())

        # Add new schedules
        State.schedules.append(new_schedule1)
        State.schedules.append(new_schedule2)


    # Helper functions
    @staticmethod
    def random_assign(schedule: Schedule):
        num_games_and_practices = len(State.games) + len(State.practices) # get total number of games and practices
        num_to_assign = random.randint(1, num_games_and_practices) # randomly get number of games and practices to mutate

        id_list = random.choices(range(1, num_games_and_practices+1), k = num_to_assign)

        new_schedule = Schedule(State.games, State.practices)
        new_schedule.clone_schedule(schedule)

        for key, value in new_schedule.get_schedule().items():
            field = State.lookup_games_and_practices(key)
            if isinstance(field, Game) and field.get_id() in id_list:
                new_schedule.add_assign(key, random.choice(list(State.game_slots.values())))
            elif isinstance(field, Practice) and field.get_id() in id_list:
                new_schedule.add_assign(key, random.choice(list(State.practice_slots.values())))

        return new_schedule
    
    
    # pass in lowest from f_wert - basic idea
    @staticmethod
    def delete(a : Schedule, b : Schedule):
        if a in State.schedules:
            State.schedules.remove(a)
        if b in State.schedules:
            State.schedules.remove(b)