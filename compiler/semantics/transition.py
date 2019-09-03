class Transition:
    """This is the transition of a state in the parser"""

    def __init__(self, transition_type, state):
        self.transition_type = transition_type
        self.state = state
