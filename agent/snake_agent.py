import torch
import random
import numpy as np
from collections import deque
from agent.model import Linear_QNet, QTrainer
from agent.helper import plot
from games.snake.snake import SnakeGame as my_game
from games.config import help_config
MAX_MEMORY = 1_000_000
BATCH_SIZE = 10000
LR = 0.001


class Agent:

    def __init__(self, model):
        config = help_config()
        self.n_games = int(config.get("snake","agent_n_games"))
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(14, 256, 3)
        if model:
            self.model.load_state_dict(torch.load('model/model.pth'))
            self.model.eval()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def danger(self, game, point, dir):
        straight_danger = sum(game.snake.look_ahead(point, dir[0], 20))
        right_danger = sum(game.snake.look_ahead(point, dir[1], 20))
        left_danger = sum(game.snake.look_ahead(point, dir[2], 20))
        return straight_danger, right_danger, left_danger

    def get_state(self, game):
        my_head = game.snake.position
        point_l = [0, 0, 1, 0]
        point_r = [0, 0, 0, 1]
        point_u = [1, 0, 0, 0]
        point_d = [0, 1, 0, 0]
        direction = game.snake.moving  # up,down,left,right
        dir_l = direction[2]
        dir_r = direction[3]
        dir_u = direction[0]
        dir_d = direction[1]
        # straight ahead
        s_danger = 0
        r_danger = 0
        l_danger = 0
        if dir_r:
            s_danger, r_danger, l_danger = self.danger(game, my_head, [point_r, point_d, point_u])
        elif dir_l:
            s_danger, r_danger, l_danger = self.danger(game, my_head, [point_l, point_u, point_d])
        elif dir_u:
            s_danger, r_danger, l_danger = self.danger(game, my_head, [point_u, point_d, point_l])
        elif dir_d:
            s_danger, r_danger, l_danger = self.danger(game, my_head, [point_d, point_l, point_r])

        state = [
            # Danger straight my
            s_danger >= 1,
            r_danger >= 1,
            l_danger >= 1,
            # Danger straight
            (dir_r and game.snake.is_collision(point_r, my_head)) or
            (dir_l and game.snake.is_collision(point_l, my_head)) or
            (dir_u and game.snake.is_collision(point_u, my_head)) or
            (dir_d and game.snake.is_collision(point_d, my_head)),

            # Danger right
            (dir_u and game.snake.is_collision(point_r, my_head)) or
            (dir_d and game.snake.is_collision(point_l, my_head)) or
            (dir_l and game.snake.is_collision(point_u, my_head)) or
            (dir_r and game.snake.is_collision(point_d, my_head)),

            # Danger left
            (dir_d and game.snake.is_collision(point_r, my_head)) or
            (dir_u and game.snake.is_collision(point_l, my_head)) or
            (dir_r and game.snake.is_collision(point_u, my_head)) or
            (dir_l and game.snake.is_collision(point_d, my_head)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.grid.food[0] < game.snake.position[0],  # food left
            game.grid.food[0] > game.snake.position[0],  # food right
            game.grid.food[1] < game.snake.position[1],  # food up
            game.grid.food[1] > game.snake.position[1]  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train(agent_model):
    config = help_config()
    config.write()
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = int(config.get("snake","record"))

    agent = Agent(agent_model)
    game = my_game()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.ai_play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                config.set("snake", "record",record)
                config.set("snake","agent_n_games",agent.n_games)
                agent.model.save()


            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train(1)
