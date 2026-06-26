# NODE

class Node:
    def __init__(self, position):
        self.position = position

        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

        self.parent = None

    def __lt__(self, other):
        return self.f < other.f