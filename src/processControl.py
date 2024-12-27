import random

from Schedule import Schedule
from State import State
from Extensions import Extensions

class processControl:
    # diff version that actually sets values and grabs smallest value
    @staticmethod
    def f_wert(schedules: list[Schedule]):
        fit_set = State.f_fit(schedules)
        unfit1, unfit2 = State.f_unfit(fit_set)
        fittest1, fittest2 = State.f_findFittest(fit_set)
        
        delete_value = 0 if len(schedules) > State.max_pop_size else 2
        func_dict = {
            "delete": (lambda: Extensions.delete(unfit1, unfit2), delete_value),
            "crossover_and_mutation": (lambda: processControl.f_select(lambda: Extensions.crossover(fittest1, fittest2), lambda: Extensions.mutation(fittest1, fittest2), 0.7, 0.3), 1)
        }
        min_key = min(func_dict, key=lambda x: func_dict[x][1])
        min_func = func_dict[min_key][0]
        return min_func() 

    # f_select, randomly pick A or B based on probabilities on return specific one.
    @staticmethod
    def f_select(A, B, p_A: float, p_B: float):
        if p_A + p_B != 1:
            raise ValueError("The probabilities must sum to 1")
        random_value = random.random()
        if callable(A) and callable(B):
            return A() if random_value < p_A else B()
        return A if random_value < p_A else B