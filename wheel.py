import random
class Wheel:
    def __init__(self,random=False):
        self.random = random
        self.states = [[-1,1],[1,-1],[-1,-1],[1,1]]
        self.set_gen()
        self.current = 0


    def set_gen(self):
        if self.random:
            random.shuffle(self.states)
        self.gen = self.get_state()

    def list_indexes(self,l):
        self.states=[i for i in range(len(l))]

    def computer_player(self):
        self.states = [[1,-1],[1,1]]
        self.set_gen()
    def next_state(self):
        try:
            return next(iter(self.gen))
        except:
            self.set_gen()
            return next(iter(self.gen))

    def get_state(self):
        for state in self.states:
            self.current =state
            yield state




