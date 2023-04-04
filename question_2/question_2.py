class PriorityQueue:
    def __init__(self):
        self.arr = []

    def insert(self, item, priority):
        self.arr.append((priority, item))
        self.arr.sort()

    def pop(self):
        return self.arr.pop()[1]

    def peek(self):
        return self.arr[-1][1]

    def isEmpty(self):
        return not bool(self.arr)


if __name__ == "__main__":
    pq = PriorityQueue()
    pq.insert("game", 20)
    pq.insert("food", 100)
    pq.insert("house", 400)

    # >>> False
    # >>> [(20, 'game'), (100, 'food'), (400, 'house')]
    # >>> house
    print(pq.isEmpty())
    print(pq.arr)
    print(pq.peek())