'''
#Backtracking(Não terminamos)
class VisitedStates:
    def __init__(self):
        self.states = set()

    def add(self, state):
        self.states.add( state )

    def is_visited(self, state):
        return state in self.states
vs = VisitedStates()
def backtracking_recursive(state):
    #TODO: verificacao de loop
    if (vs.is_visited(state)):
        return state
    vs.add(state)

    for i in range(5):
        state_transition = deepcopy(state)
        if (state_transition.make_transition(i)):
            solution = backtracking_recursive(state_transition)
            if solution.is_solution():
                return solution
 '''