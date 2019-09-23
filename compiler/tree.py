class Tree:
    """a tree data structure"""

    def __init__(self):
        self.value = None
        self.children = []

    def copy(self):
        """Deep-copy tree using breadth-first traversal"""
        queue = [self]

        copy_root = Tree()
        copy_root.value = self.value
        copy_queue = [copy_root]

        while len(queue) is not 0:
            dequeued = queue.pop(0)
            copy_dequeued = copy_queue.pop(0)
            for child in dequeued.children:
                new_copy = Tree()
                new_copy.value = child.value
                copy_dequeued.children.append(new_copy)

                queue.append(child)
                copy_queue.append(new_copy)

        return copy_root