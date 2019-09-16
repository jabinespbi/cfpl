class State:
    """The state of the parser"""

    def __init__(self):
        self.rules = []
        self.look_aheads = []  # fill this up if this is a reduce state (slr(1))
        # format: {
        #   "id": instance of Transition
        # }
        self.transitions = []
