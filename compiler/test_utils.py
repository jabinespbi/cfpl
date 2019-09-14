import unittest

from compiler.semantics.state import State
from compiler.utils import Utils


class MyTestCase(unittest.TestCase):
    def test_are_states_rules_similar(self):
        state1 = State()
        state1.rules.append(["E'", "->", ".", "E"])
        state1.rules.append(["E", "->", ".", "E", "+", "F"])
        state1.rules.append(["E", "->", ".", "F"])
        state1.rules.append(["F", "->", ".", "+", "F"])
        state1.rules.append(["F", "->", ".", "G"])
        state1.rules.append(["G", "->", ".", "id"])

        state2 = State()
        state2.rules.append(["F", "->", ".", "G"])
        state2.rules.append(["E", "->", ".", "E", "+", "F"])
        state2.rules.append(["G", "->", ".", "id"])
        state2.rules.append(["E'", "->", ".", "E"])
        state2.rules.append(["E", "->", ".", "F"])
        state2.rules.append(["F", "->", ".", "+", "F"])
        self.assertEqual(True, Utils.are_states_rules_similar(state1, state2))

    def test_is_list_contains_state(self):
        state_list = []
        state1 = State()
        state1.rules.append(["E'", "->", ".", "E"])
        state1.rules.append(["E", "->", ".", "E", "+", "F"])
        state1.rules.append(["E", "->", ".", "F"])
        state1.rules.append(["F", "->", ".", "+", "F"])
        state1.rules.append(["F", "->", ".", "G"])
        state1.rules.append(["G", "->", ".", "id"])
        state_list.append(state1)

        state2 = State()
        state2.rules.append(["F", "->", ".", "+", "F"])
        state2.rules.append(["F", "->", ".", "G"])
        state2.rules.append(["G", "->", ".", "id"])
        state_list.append(state2)

        state3 = State()
        state3.rules.append(["F", "->", ".", "G"])
        state3.rules.append(["E", "->", ".", "E", "+", "F"])
        state3.rules.append(["G", "->", ".", "id"])
        state3.rules.append(["E'", "->", ".", "E"])
        state3.rules.append(["E", "->", ".", "F"])
        state3.rules.append(["F", "->", ".", "+", "F"])
        self.assertEqual(state1, Utils.get_same_state_in_list(state_list, state3))


if __name__ == '__main__':
    unittest.main()
