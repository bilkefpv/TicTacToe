import random


class Wheel:
    def __init__(self, random=False, computer=False):
        self.random = random
        self.states = [[-1, 1], [1, -1], [-1, -1], [1, 1]]
        self.current = 0
        if computer:
            self.computer_player()
        self.set_gen()

    def set_gen(self):
        if self.random:
            random.shuffle(self.states)
        self.gen = self.get_state()

    def list_indexes(self, l):
        self.states = [i for i in range(len(l))]

    def computer_player(self):
        self.states = [[1, -1], [1, 1]]
        self.current = random.choice(self.states)

    def next_state(self):
        try:
            return next(iter(self.gen))
        except:
            self.set_gen()
            return next(iter(self.gen))

    def get_state(self):
        for state in self.states:
            self.current = state
            yield state
