import unittest

from compiler.tree import Tree


class TestTree(unittest.TestCase):
    @unittest.skip("just manual")
    def test_copy(self):
        tree_A = Tree()
        tree_A.value = "A"

        tree_B = Tree()
        tree_B.value = "B"

        tree_C = Tree()
        tree_C.value = "C"

        tree_D = Tree()
        tree_D.value = "D"

        tree_A.children.append(tree_B)
        tree_A.children.append(tree_C)
        tree_A.children.append(tree_D)

        tree_E = Tree()
        tree_E.value = "E"

        tree_F = Tree()
        tree_F.value = "F"

        tree_D.children.append(tree_E)
        tree_D.children.append(tree_F)

        tree_G = Tree()
        tree_G.value = "G"

        tree_H = Tree()
        tree_H.value = "H"

        tree_E.children.append(tree_G)
        tree_E.children.append(tree_H)

        copied = tree_A.copy_tree()


if __name__ == '__main__':
    unittest.main()
