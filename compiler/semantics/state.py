class State:
    """The state of the parser"""

    def __init__(self):
        self.rules = []

        # format: {
        #   "id": instance of Transition
        # }
        self.transitions = {}
