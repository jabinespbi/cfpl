from compiler.semantics.state_type import StateType


class State:
    """The state of the parser"""

    def __init__(self):
        self.rules = []
        self.type = StateType.NORMAL   # change this if the state is reduce or accept state
        self.look_aheads = []  # fill this up if this is a reduce state (slr(1))
        # format: {
        #   "id": instance of Transition
        # }
        self.transitions = {}
